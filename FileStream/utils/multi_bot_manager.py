import asyncio
import logging
import random
from typing import Dict, List, Optional
from pyrogram import Client
from FileStream.config import Telegram

class MultiBotManager:
    def __init__(self):
        self.processing_bots: Dict[str, Client] = {}  # Only for backend processing
        self.bot_loads: Dict[str, int] = {}
        self.active = False
        self.main_bot = None  # Main bot handles all user interactions
        
    async def initialize_multi_bots(self, main_bot: Client):
        """Initialize multiple bot instances for backend processing only"""
        self.main_bot = main_bot
        
        if not Telegram.MULTI_BOT_MODE or not Telegram.MULTI_TOKENS:
            logging.info("Multi-bot mode disabled or no additional tokens provided")
            self.active = False
            return
        
        logging.info(f"Initializing {len(Telegram.MULTI_TOKENS)} processing bots for speed boost...")
        
        for i, token in enumerate(Telegram.MULTI_TOKENS, 1):
            bot_id = f"processor_{i}"
            try:
                bot = Client(
                    name=f"processor_bot_{i}",
                    api_id=Telegram.API_ID,
                    api_hash=Telegram.API_HASH,
                    bot_token=token,
                    sleep_threshold=Telegram.SLEEP_THRESHOLD,
                    no_updates=True,  # No message handlers, only for processing
                    in_memory=True,
                )
                
                await bot.start()
                bot_info = await bot.get_me()
                
                # Ensure bot.me is set for compatibility
                bot.me = bot_info
                
                self.processing_bots[bot_id] = bot
                self.bot_loads[bot_id] = 0
                
                logging.info(f"✅ Processing Bot {i} initialized: @{bot_info.username}")
                
            except Exception as e:
                logging.error(f"❌ Failed to initialize processing bot {i}: {e}")
                continue
        
        self.active = len(self.processing_bots) > 0
        logging.info(f"Processing bot system {'activated' if self.active else 'failed'} with {len(self.processing_bots)} bots")
    
    def get_least_loaded_processor(self) -> Client:
        """Get the processing bot with least current load for backend tasks"""
        if not self.active or not self.bot_loads:
            return self.main_bot  # Fallback to main bot if no processors available
        
        # Find processing bot with minimum load
        try:
            min_load_bot = min(self.bot_loads.items(), key=lambda x: x[1])
            return self.processing_bots[min_load_bot[0]]
        except (ValueError, KeyError):
            return self.main_bot  # Fallback if min() fails
    
    def get_random_processor(self) -> Client:
        """Get a random processing bot for load distribution"""
        if not self.active or not self.processing_bots:
            return self.main_bot  # Fallback to main bot if no processors available
        
        try:
            bot_id = random.choice(list(self.processing_bots.keys()))
            return self.processing_bots[bot_id]
        except (IndexError, KeyError):
            return self.main_bot  # Fallback if random choice fails
    
    def get_main_bot(self) -> Client:
        """Always return the main bot for user interactions"""
        return self.main_bot
    
    def increment_processor_load(self, bot: Client):
        """Increment load counter for a processing bot"""
        for bot_id, bot_instance in self.processing_bots.items():
            if bot_instance.me.id == bot.me.id:
                self.bot_loads[bot_id] += 1
                break
    
    def decrement_processor_load(self, bot: Client):
        """Decrement load counter for a processing bot"""
        for bot_id, bot_instance in self.processing_bots.items():
            if bot_instance.me.id == bot.me.id:
                self.bot_loads[bot_id] = max(0, self.bot_loads[bot_id] - 1)
                break
    
    def get_bot_stats(self) -> Dict:
        """Get current processing bot load statistics"""
        return {
            "active": self.active,
            "main_bot": self.main_bot.me.username if hasattr(self.main_bot, 'me') else "Main Bot",
            "total_processors": len(self.processing_bots),
            "processor_loads": self.bot_loads.copy()
        }
    
    async def stop_all_bots(self):
        """Stop all processing bot instances (not the main bot)"""
        for bot_id, bot in self.processing_bots.items():
            try:
                await bot.stop()
                logging.info(f"Stopped processing bot: {bot_id}")
            except Exception as e:
                logging.error(f"Error stopping processing bot {bot_id}: {e}")
        
        self.processing_bots.clear()
        self.bot_loads.clear()
        self.active = False

# Global instance
multi_bot_manager = MultiBotManager()
