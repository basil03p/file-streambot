
import asyncio
import time
from FileStream.bot import FileStream, multi_clients
from FileStream.utils.bot_utils import is_user_banned, is_user_exist, is_user_joined, gen_link, is_channel_banned, is_channel_exist, is_user_authorized
from FileStream.utils.database import Database
from FileStream.utils.file_properties import get_file_ids, get_file_info
from FileStream.utils.multi_bot_manager import multi_bot_manager
from FileStream.config import Telegram, Server
from pyrogram import filters, Client
from pyrogram.errors import FloodWait
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums.parse_mode import ParseMode
db = Database(Telegram.DATABASE_URL, Telegram.SESSION_NAME)

@FileStream.on_message(
    filters.private
    & (
            filters.document
            | filters.video
            | filters.video_note
            | filters.audio
            | filters.voice
            | filters.animation
            | filters.photo
    ),
    group=4,
)
async def private_receive_handler(bot: Client, message: Message):
    if not await is_user_authorized(message):
        return
    if await is_user_banned(message):
        return

    await is_user_exist(bot, message)
    if Telegram.FORCE_SUB:
        if not await is_user_joined(bot, message):
            return
    
    # Check if user already has an active request
    if await db.is_user_requesting(message.from_user.id):
        active_request = await db.get_user_active_request(message.from_user.id)
        await message.reply_text(
            text="⚠️ **You already have an active file request!**\n\n"
                 "Please wait for your current request to complete or use /revoke to cancel it.\n\n"
                 f"📝 **Current request:** {active_request.get('request_type', 'file_upload')}\n"
                 f"⏱️ **Started:** {int((time.time() - active_request['start_time']) / 60)} minutes ago",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🚫 Revoke Current Request", callback_data=f"revoke_request_{message.from_user.id}")]
            ]),
            quote=True
        )
        return
    
    # Select processing bot for backend tasks (not for user interaction)
    processing_bot = multi_bot_manager.get_least_loaded_processor() if Telegram.MULTI_BOT_MODE else bot
    
    try:
        # Add user to active requests
        file_info_preview = {
            "file_name": getattr(message.document or message.video or message.audio or message.photo, 'file_name', 'Unknown'),
            "file_size": getattr(message.document or message.video or message.audio or message.photo, 'file_size', 0)
        }
        await db.add_active_request(message.from_user.id, "file_upload", file_info_preview)
        
        # Increment processing bot load (only if different from main bot)
        if processing_bot.me.id != bot.me.id:
            multi_bot_manager.increment_processor_load(processing_bot)
        
        # Send processing message (always from main bot)
        processing_msg = await message.reply_text(
            text="📤 **Processing your file...**\n\n"
                 f"🤖 **Backend Processor:** {processing_bot.me.first_name if hasattr(processing_bot, 'me') and processing_bot.me.id != bot.me.id else 'Main Bot'}\n"
                 "Please wait while I generate the download link.\n\n"
                 "💡 **Tip:** Use /revoke to cancel this request if needed.",
            parse_mode=ParseMode.MARKDOWN,
            quote=True
        )
        
        # Update request status
        await db.update_request_status(message.from_user.id, "generating_link")
        
        # Backend processing (use processing bot for file operations)
        inserted_id = await db.add_file(get_file_info(message))
        await get_file_ids(processing_bot, inserted_id, multi_clients, message)  # Use processing bot here
        reply_markup, stream_text = await gen_link(_id=inserted_id)
        
        # Delete processing message and send final result (always from main bot)
        await processing_msg.delete()
        
        # Add processing info to the response
        processor_info = ""
        if Telegram.MULTI_BOT_MODE and processing_bot.me.id != bot.me.id:
            processor_info = f"\n\n⚡ **Speed Boost:** Processed using backend bot @{processing_bot.me.username if hasattr(processing_bot, 'me') else 'ProcessorBot'}"
        
        await message.reply_text(
            text=stream_text + processor_info,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True,
            reply_markup=reply_markup,
            quote=True
        )
        
        # Update request status to completed
        await db.update_request_status(message.from_user.id, "completed")
        
    except FloodWait as e:
        print(f"Sleeping for {str(e.value)}s")
        await asyncio.sleep(e.value)
        await bot.send_message(chat_id=Telegram.ULOG_CHANNEL,
                               text=f"Gᴏᴛ FʟᴏᴏᴅWᴀɪᴛ ᴏғ {str(e.value)}s ғʀᴏᴍ [{message.from_user.first_name}](tg://user?id={message.from_user.id})\n\n**ᴜsᴇʀ ɪᴅ :** `{str(message.from_user.id)}`",
                               disable_web_page_preview=True, parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        print(f"Error processing file: {e}")
        await message.reply_text(
            text="❌ **Error processing your file!**\n\nPlease try again later.",
            parse_mode=ParseMode.MARKDOWN,
            quote=True
        )
    finally:
        # Always remove user from active requests and decrement bot load
        await db.remove_active_request(message.from_user.id)
        if processing_bot.me.id != bot.me.id:
            multi_bot_manager.decrement_processor_load(processing_bot)


@FileStream.on_message(
    filters.channel
    & ~filters.forwarded
    & ~filters.media_group
    & (
            filters.document
            | filters.video
            | filters.video_note
            | filters.audio
            | filters.voice
            | filters.photo
    )
)
async def channel_receive_handler(bot: Client, message: Message):
    if await is_channel_banned(bot, message):
        return
    await is_channel_exist(bot, message)

    # Check if this is from authorized channel
    is_auth_channel = (Telegram.AUTH_CHANNEL and 
                      str(message.chat.id) == str(Telegram.AUTH_CHANNEL))
    
    # Use processing bot for auth channel backend tasks (not user interaction)
    processing_bot = multi_bot_manager.get_random_processor() if (is_auth_channel and Telegram.MULTI_BOT_MODE) else bot

    try:
        # Increment processing bot load (only if using backend processor)
        if Telegram.MULTI_BOT_MODE and processing_bot.me.id != bot.me.id:
            multi_bot_manager.increment_processor_load(processing_bot)
        
        # Use enhanced file adding for auth channel
        if is_auth_channel:
            inserted_id = await db.add_channel_file(get_file_info(message), message.chat.id)
        else:
            inserted_id = await db.add_file(get_file_info(message))
            
        await get_file_ids(processing_bot, inserted_id, multi_clients, message)  # Use processing bot for file operations
        
        # Generate appropriate buttons based on channel type
        if is_auth_channel and Telegram.GENERATE_DOWNLOAD_LINKS:
            # Enhanced buttons for auth channel with download links
            reply_markup, stream_link = await gen_link(_id=inserted_id)
            buttons = [
                [InlineKeyboardButton("🎬 Stream", url=f"{Server.URL}watch/{str(inserted_id)}")],
                [InlineKeyboardButton("📥 Download", url=f"{Server.URL}dl/{str(inserted_id)}")],
                [InlineKeyboardButton("📱 Get File", url=f"https://t.me/{FileStream.username}?start=file_{str(inserted_id)}")],
                [InlineKeyboardButton("🔗 Bot Link", url=f"https://t.me/{FileStream.username}?start=stream_{str(inserted_id)}")]
            ]
            enhanced_markup = InlineKeyboardMarkup(buttons)
        else:
            # Standard button for non-auth channels
            enhanced_markup = InlineKeyboardMarkup(
                [[InlineKeyboardButton("Dᴏᴡɴʟᴏᴀᴅ ʟɪɴᴋ 📥",
                                       url=f"https://t.me/{FileStream.username}?start=stream_{str(inserted_id)}")]]
            )

        await bot.edit_message_reply_markup(
            chat_id=message.chat.id,
            message_id=message.id,
            reply_markup=enhanced_markup
        )

        # Log multi-bot usage for auth channels (always sent by main bot)
        if is_auth_channel and Telegram.MULTI_BOT_MODE and processing_bot.me.id != bot.me.id:
            await bot.send_message(  # Always use main bot for user communication
                chat_id=Telegram.ULOG_CHANNEL,
                text=f"📤 **Auth Channel File Processed**\n\n"
                     f"🤖 **Backend Processor:** {processing_bot.me.first_name if hasattr(processing_bot, 'me') else 'ProcessorBot'}\n"
                     f"📁 **File:** {message.document.file_name if message.document else 'Media File'}\n"
                     f"📊 **Channel:** {message.chat.title}",
                disable_web_page_preview=True
            )

    except FloodWait as w:
        print(f"Sleeping for {str(w.x)}s")
        await asyncio.sleep(w.x)
        await bot.send_message(chat_id=Telegram.ULOG_CHANNEL,
                               text=f"ɢᴏᴛ ғʟᴏᴏᴅᴡᴀɪᴛ ᴏғ {str(w.x)}s ғʀᴏᴍ {message.chat.title}\n\n**ᴄʜᴀɴɴᴇʟ ɪᴅ :** `{str(message.chat.id)}`",
                               disable_web_page_preview=True)
    except Exception as e:
        await bot.send_message(chat_id=Telegram.ULOG_CHANNEL, text=f"**#EʀʀᴏʀTʀᴀᴄᴋᴇʙᴀᴄᴋ:** `{e}`",
                               disable_web_page_preview=True)
        print(f"Cᴀɴ'ᴛ Eᴅɪᴛ Bʀᴏᴀᴅᴄᴀsᴛ Mᴇssᴀɢᴇ!\nEʀʀᴏʀ:  **Gɪᴠᴇ ᴍᴇ ᴇᴅɪᴛ ᴘᴇʀᴍɪssɪᴏɴ ɪɴ ᴜᴘᴅᴀᴛᴇs ᴀɴᴅ ʙɪɴ Cʜᴀɴɴᴇʟ!{e}**")
    finally:
        # Decrement processing bot load (only if using backend processor)
        if Telegram.MULTI_BOT_MODE and processing_bot.me.id != bot.me.id:
            multi_bot_manager.decrement_processor_load(processing_bot)

