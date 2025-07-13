"""
Migration script to add expiration times to existing files in the database.
This script should be run once after implementing the new expiration system.
"""
import asyncio
import time
from FileStream.utils.database import Database
from FileStream.config import Telegram

async def migrate_existing_files():
    """Add expiration times to existing files that don't have them"""
    db = Database(Telegram.DATABASE_URL, Telegram.SESSION_NAME)
    
    print("Starting migration of existing files...")
    
    # Find all files without expiration times
    current_time = time.time()
    files_without_expiry = await db.file.find({"expires_at": {"$exists": False}}).to_list(None)
    
    print(f"Found {len(files_without_expiry)} files without expiration times")
    
    updated_count = 0
    for file_doc in files_without_expiry:
        # Set expiration to 1 hour from the file's creation time
        file_creation_time = file_doc.get("time", current_time)
        expires_at = file_creation_time + 3600  # 1 hour from creation
        
        # If the file would have already expired, set it to expire in 1 minute
        if expires_at <= current_time:
            expires_at = current_time + 60  # Give 1 minute grace period
        
        await db.file.update_one(
            {"_id": file_doc["_id"]},
            {"$set": {"expires_at": expires_at}}
        )
        updated_count += 1
    
    print(f"Migration completed! Updated {updated_count} files with expiration times.")
    
    # Clean up any files that are already expired
    deleted_count = await db.delete_expired_files()
    print(f"Cleaned up {deleted_count} expired files during migration.")

if __name__ == "__main__":
    asyncio.run(migrate_existing_files())
