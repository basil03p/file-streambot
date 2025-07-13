import asyncio
import logging
import time
from FileStream.utils.database import Database
from FileStream.config import Telegram

class BackgroundTasks:
    def __init__(self):
        self.db = Database(Telegram.DATABASE_URL, Telegram.SESSION_NAME)
        self.cleanup_interval = 300  # Run cleanup every 5 minutes
        self.running = False

    async def start_background_tasks(self):
        """Start all background tasks"""
        self.running = True
        asyncio.create_task(self.file_cleanup_task())
        asyncio.create_task(self.request_cleanup_task())
        logging.info("Background tasks started")

    async def stop_background_tasks(self):
        """Stop all background tasks"""
        self.running = False
        logging.info("Background tasks stopped")

    async def file_cleanup_task(self):
        """Background task to clean up expired files"""
        while self.running:
            try:
                deleted_count = await self.db.delete_expired_files()
                if deleted_count > 0:
                    logging.info(f"Cleaned up {deleted_count} expired files")
            except Exception as e:
                logging.error(f"Error in file cleanup task: {e}")
            
            await asyncio.sleep(self.cleanup_interval)

    async def request_cleanup_task(self):
        """Background task to clean up old active requests"""
        while self.running:
            try:
                cleaned_count = await self.db.cleanup_old_requests()
                if cleaned_count > 0:
                    logging.info(f"Cleaned up {cleaned_count} old active requests")
            except Exception as e:
                logging.error(f"Error in request cleanup task: {e}")
            
            await asyncio.sleep(60)  # Run every minute

# Global instance
background_tasks = BackgroundTasks()
