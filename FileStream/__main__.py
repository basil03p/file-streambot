import sys
import asyncio
import logging
import traceback
import logging.handlers as handlers
from FileStream.config import Telegram, Server
from aiohttp import web
from pyrogram import idle
from FileStream.bot import FileStream
from FileStream.server import web_server
from FileStream.bot.clients import initialize_clients
from flask import Flask
import threading
import signal

# Flask Server to Keep Service Alive
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running"

def run_flask():
    app.run(host="0.0.0.0", port=8080, use_reloader=False)

# Start Flask in a background thread
flask_thread = threading.Thread(target=run_flask)
flask_thread.daemon = True
flask_thread.start()

# Logging Configuration
logging.basicConfig(
    level=logging.INFO,
    datefmt="%d/%m/%Y %H:%M:%S",
    format='[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(stream=sys.stdout),
        handlers.RotatingFileHandler("streambot.log", mode="a", maxBytes=104857600, backupCount=2, encoding="utf-8"),
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
    FileStream.id = bot_info.id
    FileStream.username = bot_info.username
    FileStream.fname = bot_info.first_name
    print("------------------------------ DONE ------------------------------\n")

    print("---------------------- Initializing Clients ----------------------")
    await initialize_clients()
    print("------------------------------ DONE ------------------------------\n")

    print("--------------------- Initializing Web Server ---------------------")
    await server.setup()
    await web.TCPSite(server, Server.BIND_ADDRESS, Server.PORT).start()
    print("------------------------------ DONE ------------------------------\n")

    print("------------------------- Service Started -------------------------")
    print("                        bot =>> {}".format(bot_info.first_name))
    if bot_info.dc_id:
        print("                        DC ID =>> {}".format(str(bot_info.dc_id)))
    print(" URL =>> {}".format(Server.URL))
    print("------------------------------------------------------------------")
    
    await idle()

async def cleanup():
    print("Received shutdown signal. Cleaning up...")
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
