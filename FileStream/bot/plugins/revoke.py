import asyncio
import time
from FileStream.bot import FileStream
from FileStream.utils.database import Database
from FileStream.utils.multi_bot_manager import multi_bot_manager
from FileStream.config import Telegram
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.enums.parse_mode import ParseMode

db = Database(Telegram.DATABASE_URL, Telegram.SESSION_NAME)

@FileStream.on_message(filters.command('revoke') & filters.private)
async def revoke_request_command(bot: Client, message: Message):
    """Command to revoke active request"""
    user_id = message.from_user.id
    
    # Check if user has an active request
    active_request = await db.get_user_active_request(user_id)
    
    if not active_request:
        await message.reply_text(
            text="❌ **No Active Request Found**\n\nYou don't have any active file requests to revoke.",
            parse_mode=ParseMode.MARKDOWN,
            quote=True
        )
        return
    
    # Show confirmation
    elapsed_time = int((time.time() - active_request['start_time']) / 60)
    await message.reply_text(
        text=f"🚫 **Revoke Request Confirmation**\n\n"
             f"📝 **Request Type:** {active_request.get('request_type', 'file_upload')}\n"
             f"⏱️ **Running for:** {elapsed_time} minutes\n"
             f"📊 **Status:** {active_request.get('status', 'processing')}\n\n"
             "Are you sure you want to cancel this request?",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("✅ Yes, Revoke", callback_data=f"confirm_revoke_{user_id}"),
                InlineKeyboardButton("❌ No, Keep", callback_data=f"cancel_revoke_{user_id}")
            ]
        ]),
        quote=True
    )

@FileStream.on_message(filters.command('status') & filters.private)
async def request_status_command(bot: Client, message: Message):
    """Command to check request status"""
    user_id = message.from_user.id
    
    # Check if user has an active request
    active_request = await db.get_user_active_request(user_id)
    
    if not active_request:
        await message.reply_text(
            text="✅ **No Active Requests**\n\nYou can send a new file for processing.",
            parse_mode=ParseMode.MARKDOWN,
            quote=True
        )
        return
    
    elapsed_time = int((time.time() - active_request['start_time']) / 60)
    file_info = active_request.get('file_info', {})
    
    status_text = f"📊 **Request Status**\n\n" \
                  f"📝 **Type:** {active_request.get('request_type', 'file_upload')}\n" \
                  f"📊 **Status:** {active_request.get('status', 'processing')}\n" \
                  f"⏱️ **Duration:** {elapsed_time} minutes\n"
    
    if file_info:
        status_text += f"📁 **File:** {file_info.get('file_name', 'Unknown')}\n" \
                       f"📏 **Size:** {file_info.get('file_size', 0)} bytes\n"
    
    status_text += "\n💡 **Tip:** Use /revoke to cancel this request"
    
    await message.reply_text(
        text=status_text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🚫 Revoke Request", callback_data=f"revoke_request_{user_id}")]
        ]),
        quote=True
    )

@FileStream.on_message(filters.command('botstats') & filters.private & filters.user(Telegram.OWNER_ID))
async def bot_stats_command(bot: Client, message: Message):
    """Command to check multi-bot statistics"""
    if not Telegram.MULTI_BOT_MODE:
        await message.reply_text(
            text="📊 **Bot Statistics**\n\n🤖 **Mode:** Single Bot\n❌ **Multi-bot:** Disabled",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    stats = multi_bot_manager.get_bot_stats()
    
    stats_text = f"📊 **Multi-Bot Statistics**\n\n" \
                 f"🤖 **Total Bots:** {stats['total_bots']}\n" \
                 f"✅ **Status:** {'Active' if stats['active'] else 'Inactive'}\n\n" \
                 f"📈 **Current Loads:**\n"
    
    for bot_id, load in stats['loads'].items():
        stats_text += f"└ **{bot_id}:** {load} requests\n"
    
    # Get active requests count
    total_requests = len(await db.requests.find({}).to_list(None))
    stats_text += f"\n🔄 **Active Requests:** {total_requests}"
    
    await message.reply_text(
        text=stats_text,
        parse_mode=ParseMode.MARKDOWN
    )

# Callback handlers for revoke confirmation
@FileStream.on_callback_query(filters.regex(r"^revoke_request_"))
async def revoke_request_callback(bot: Client, callback: CallbackQuery):
    """Handle revoke request button"""
    user_id = int(callback.data.split("_")[-1])
    
    if callback.from_user.id != user_id:
        await callback.answer("❌ You can only revoke your own requests!", show_alert=True)
        return
    
    # Show confirmation
    active_request = await db.get_user_active_request(user_id)
    
    if not active_request:
        await callback.edit_message_text(
            text="❌ **Request Not Found**\n\nThis request may have already been completed or expired.",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    elapsed_time = int((time.time() - active_request['start_time']) / 60)
    await callback.edit_message_text(
        text=f"🚫 **Revoke Request Confirmation**\n\n"
             f"📝 **Request Type:** {active_request.get('request_type', 'file_upload')}\n"
             f"⏱️ **Running for:** {elapsed_time} minutes\n"
             f"📊 **Status:** {active_request.get('status', 'processing')}\n\n"
             "Are you sure you want to cancel this request?",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("✅ Yes, Revoke", callback_data=f"confirm_revoke_{user_id}"),
                InlineKeyboardButton("❌ No, Keep", callback_data=f"cancel_revoke_{user_id}")
            ]
        ])
    )

@FileStream.on_callback_query(filters.regex(r"^confirm_revoke_"))
async def confirm_revoke_callback(bot: Client, callback: CallbackQuery):
    """Confirm request revocation"""
    user_id = int(callback.data.split("_")[-1])
    
    if callback.from_user.id != user_id:
        await callback.answer("❌ You can only revoke your own requests!", show_alert=True)
        return
    
    # Revoke the request
    success = await db.revoke_user_request(user_id)
    
    if success:
        await callback.edit_message_text(
            text="✅ **Request Revoked Successfully**\n\n"
                 "Your active request has been cancelled. You can now send a new file for processing.",
            parse_mode=ParseMode.MARKDOWN
        )
        await callback.answer("✅ Request revoked successfully!")
    else:
        await callback.edit_message_text(
            text="❌ **Failed to Revoke**\n\n"
                 "The request may have already been completed or expired.",
            parse_mode=ParseMode.MARKDOWN
        )
        await callback.answer("❌ Request not found!")

@FileStream.on_callback_query(filters.regex(r"^cancel_revoke_"))
async def cancel_revoke_callback(bot: Client, callback: CallbackQuery):
    """Cancel request revocation"""
    user_id = int(callback.data.split("_")[-1])
    
    if callback.from_user.id != user_id:
        await callback.answer("❌ You can only manage your own requests!", show_alert=True)
        return
    
    await callback.edit_message_text(
        text="✅ **Request Preserved**\n\n"
             "Your request is still being processed. Use /status to check progress.",
        parse_mode=ParseMode.MARKDOWN
    )
    await callback.answer("✅ Request kept active!")
