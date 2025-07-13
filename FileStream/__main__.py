import sys
import asyncio
import logging
import traceback
import os
import logging.handlers as handlers
from FileStream.config import Telegram, Server
from aiohttp import web
from pyrogram import idle
from FileStream.bot import FileStream
from FileStream.server import web_server
from FileStream.bot.clients import initialize_clients
from FileStream.utils.background_tasks import background_tasks
from FileStream.utils.multi_bot_manager import multi_bot_manager
import signal

# Remove Flask to avoid port conflicts - aiohttp will handle everything
# Koyeb-optimized logging configuration
logging.basicConfig(
    level=logging.INFO,
    datefmt="%d/%m/%Y %H:%M:%S",
    format='[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(stream=sys.stdout),
        # Reduced log file size for Koyeb
        handlers.RotatingFileHandler("streambot.log", mode="a", maxBytes=10485760, backupCount=1, encoding="utf-8"),
    ],
)

logging.getLogger("aiohttp").setLevel(logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("aiohttp.web").setLevel(logging.ERROR)

server = web.AppRunner(web_server())
loop = asyncio.get_event_loop()

async def start_services():
    print("\n------------------- Starting as Primary Server -------------------\n")
    print("-------------------- Initializing Telegram Bot --------------------")
    
    await FileStream.start()
    bot_info = await FileStream.get_me()
    FileStream.me = bot_info  # Set the full me object
    FileStream.id = bot_info.id
    FileStream.username = bot_info.username
    FileStream.fname = bot_info.first_name
    print("------------------------------ DONE ------------------------------\n")

    print("---------------------- Initializing Clients ----------------------")
    await initialize_clients()
    print("------------------------------ DONE ------------------------------\n")

    print("--------------------- Initializing Multi-Bot System ---------------")
    if Telegram.MULTI_BOT_MODE:
        await multi_bot_manager.initialize_multi_bots(FileStream)
        stats = multi_bot_manager.get_bot_stats()
        print(f"Multi-bot system: {'✅ Active' if stats['active'] else '❌ Inactive'}")
        print(f"Main bot (user interactions): {stats['main_bot']}")
        print(f"Backend processors available: {stats['total_processors']}")
        if Telegram.AUTH_CHANNEL:
            print(f"Auth channel configured: {Telegram.AUTH_CHANNEL}")
    else:
        print("Multi-bot mode: ❌ Disabled")
    print("------------------------------ DONE ------------------------------\n")

    print("--------------------- Starting Background Tasks -------------------")
    await background_tasks.start_background_tasks()
    print("------------------------------ DONE ------------------------------\n")

    print("--------------------- Initializing Web Server ---------------------")
    await server.setup()
    # Use environment port if available (Koyeb compatibility)
    port = int(os.environ.get("PORT", Server.PORT))
    bind_addr = os.environ.get("HOST", Server.BIND_ADDRESS)
    
    await web.TCPSite(server, bind_addr, port).start()
    print("------------------------------ DONE ------------------------------\n")

    print("------------------------- Service Started -------------------------")
    print("                        bot =>> {}".format(bot_info.first_name))
    if bot_info.dc_id:
        print("                        DC ID =>> {}".format(str(bot_info.dc_id)))
    print("                        Port =>> {}".format(port))
    print("                        Host =>> {}".format(bind_addr))
    print("------------------------------------------------------------------")
    
    # Keep the service alive without blocking
    while True:
        await asyncio.sleep(30)  # Keep alive ping every 30 seconds

async def cleanup():
    print("Received shutdown signal. Cleaning up...")
    await background_tasks.stop_background_tasks()
    await multi_bot_manager.stop_all_bots()
    await server.cleanup()
    await FileStream.stop()

def shutdown_handler(signum, frame):
    loop.create_task(cleanup())

# Handle SIGTERM to prevent Koyeb auto-shutdown
signal.signal(signal.SIGTERM, shutdown_handler)

if __name__ == "__main__":
    try:
        loop.run_until_complete(start_services())
    except KeyboardInterrupt:
        pass
    except Exception as err:
        logging.error(traceback.format_exc())
    finally:
        loop.run_until_complete(cleanup())
        loop.stop()
        print("------------------------ Stopped Services ------------------------")
