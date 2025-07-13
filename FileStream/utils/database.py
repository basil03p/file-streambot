import pymongo
import time
import motor.motor_asyncio
from bson.objectid import ObjectId
from bson.errors import InvalidId
from FileStream.server.exceptions import FIleNotFound

class Database:
    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.users
        self.black = self.db.blacklist
        self.file = self.db.file
        self.requests = self.db.active_requests  # New collection for tracking active requests

#---------------------[ NEW USER ]---------------------#
    def new_user(self, id):
        return dict(
            id=id,
            join_date=time.time(),
            Links=0
        )

# ---------------------[ ADD USER ]---------------------#
    async def add_user(self, id):
        user = self.new_user(id)
        await self.col.insert_one(user)

# ---------------------[ GET USER ]---------------------#
    async def get_user(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user

# ---------------------[ CHECK USER ]---------------------#
    async def total_users_count(self):
        count = await self.col.count_documents({})
        return count

    async def get_all_users(self):
        all_users = self.col.find({})
        return all_users

# ---------------------[ REMOVE USER ]---------------------#
    async def delete_user(self, user_id):
        await self.col.delete_many({'id': int(user_id)})

# ---------------------[ BAN, UNBAN USER ]---------------------#
    def black_user(self, id):
        return dict(
            id=id,
            ban_date=time.time()
        )

    async def ban_user(self, id):
        user = self.black_user(id)
        await self.black.insert_one(user)

    async def unban_user(self, id):
        await self.black.delete_one({'id': int(id)})

    async def is_user_banned(self, id):
        user = await self.black.find_one({'id': int(id)})
        return True if user else False

    async def total_banned_users_count(self):
        count = await self.black.count_documents({})
        return count
        
# ---------------------[ ADD FILE TO DB ]---------------------#
    async def add_file(self, file_info):
        file_info["time"] = time.time()
        file_info["expires_at"] = time.time() + 3600  # Add expiration time (1 hour)
        fetch_old = await self.get_file_by_fileuniqueid(file_info["user_id"], file_info["file_unique_id"])
        if fetch_old:
            return fetch_old["_id"]
        await self.count_links(file_info["user_id"], "+")
        return (await self.file.insert_one(file_info)).inserted_id

# ---------------------[ FIND FILE IN DB ]---------------------#
    async def find_files(self, user_id, range):
        user_files=self.file.find({"user_id": user_id})
        user_files.skip(range[0] - 1)
        user_files.limit(range[1] - range[0] + 1)
        user_files.sort('_id', pymongo.DESCENDING)
        total_files = await self.file.count_documents({"user_id": user_id})
        return user_files, total_files

    async def get_file(self, _id):
        try:
            file_info=await self.file.find_one({"_id": ObjectId(_id)})
            if not file_info:
                raise FIleNotFound
            return file_info
        except InvalidId:
            raise FIleNotFound
    
    async def get_file_by_fileuniqueid(self, id, file_unique_id, many=False):
        if many:
            return self.file.find({"file_unique_id": file_unique_id})
        else:
            file_info=await self.file.find_one({"user_id": id, "file_unique_id": file_unique_id})
        if file_info:
            return file_info
        return False

# ---------------------[ TOTAL FILES ]---------------------#
    async def total_files(self, id=None):
        if id:
            return await self.file.count_documents({"user_id": id})
        return await self.file.count_documents({})

# ---------------------[ DELETE FILES ]---------------------#
    async def delete_one_file(self, _id):
        await self.file.delete_one({'_id': ObjectId(_id)})

# ---------------------[ UPDATE FILES ]---------------------#
    async def update_file_ids(self, _id, file_ids: dict):
        await self.file.update_one({"_id": ObjectId(_id)}, {"$set": {"file_ids": file_ids}})

# ---------------------[ PAID SYS ]---------------------#
#     async def link_available(self, id):
#         user = await self.col.find_one({"id": id})
#         if user.get("Plan") == "Plus":
#             return "Plus"
#         elif user.get("Plan") == "Free":
#             files = await self.file.count_documents({"user_id": id})
#             if files < 11:
#                 return True
#             return False
        
    async def count_links(self, id, operation: str):
        if operation == "-":
            await self.col.update_one({"id": id}, {"$inc": {"Links": -1}})
        elif operation == "+":
            await self.col.update_one({"id": id}, {"$inc": {"Links": 1}})

# ---------------------[ NEW REQUEST TRACKING METHODS ]---------------------#
    async def is_user_requesting(self, user_id):
        """Check if user has an active request"""
        active_request = await self.requests.find_one({"user_id": user_id})
        if active_request:
            # Check if request is still valid (not older than 5 minutes)
            if time.time() - active_request["start_time"] < 300:  # 5 minutes timeout
                return True
            else:
                # Remove expired request
                await self.requests.delete_one({"user_id": user_id})
        return False

    async def add_active_request(self, user_id, request_type="file_upload", file_info=None):
        """Add user to active requests with additional info"""
        request_data = {
            "user_id": user_id,
            "start_time": time.time(),
            "request_type": request_type,
            "status": "processing"
        }
        if file_info:
            request_data["file_info"] = file_info
        
        await self.requests.insert_one(request_data)

    async def update_request_status(self, user_id, status):
        """Update request status"""
        await self.requests.update_one(
            {"user_id": user_id},
            {"$set": {"status": status, "updated_time": time.time()}}
        )

    async def get_user_active_request(self, user_id):
        """Get user's active request details"""
        return await self.requests.find_one({"user_id": user_id})

    async def revoke_user_request(self, user_id):
        """Revoke/cancel user's active request"""
        active_request = await self.requests.find_one({"user_id": user_id})
        if active_request:
            await self.requests.delete_one({"user_id": user_id})
            return True
        return False

    async def remove_active_request(self, user_id):
        """Remove user from active requests"""
        await self.requests.delete_one({"user_id": user_id})

# ---------------------[ CHANNEL FILE METHODS ]---------------------#
    async def add_channel_file(self, file_info, channel_id):
        """Add file from authorized channel with special handling"""
        file_info["time"] = time.time()
        file_info["expires_at"] = time.time() + 3600  # 1 hour expiration
        file_info["from_auth_channel"] = True
        file_info["auth_channel_id"] = channel_id
        file_info["download_enabled"] = True  # Enable download links for auth channel files
        
        fetch_old = await self.get_file_by_fileuniqueid(file_info["user_id"], file_info["file_unique_id"])
        if fetch_old:
            return fetch_old["_id"]
        
        await self.count_links(file_info["user_id"], "+")
        return (await self.file.insert_one(file_info)).inserted_id

    async def is_auth_channel_file(self, file_id):
        """Check if file is from authorized channel"""
        try:
            file_info = await self.get_file(file_id)
            return file_info.get("from_auth_channel", False)
        except:
            return False

    async def get_channel_files_count(self, channel_id):
        """Get count of files from specific channel"""
        return await self.file.count_documents({"auth_channel_id": channel_id})

# ---------------------[ FILE CLEANUP METHODS ]---------------------#
    async def get_expired_files(self):
        """Get all files that have expired (older than 1 hour)"""
        current_time = time.time()
        expired_files = self.file.find({"expires_at": {"$lt": current_time}})
        return expired_files

    async def delete_expired_files(self):
        """Delete all expired files from database"""
        current_time = time.time()
        expired_files = await self.file.find({"expires_at": {"$lt": current_time}}).to_list(None)
        
        deleted_count = 0
        for file_doc in expired_files:
            # Decrease user's link count
            await self.count_links(file_doc["user_id"], "-")
            deleted_count += 1
        
        # Delete all expired files
        result = await self.file.delete_many({"expires_at": {"$lt": current_time}})
        return result.deleted_count

    async def cleanup_old_requests(self):
        """Clean up old active requests (older than 5 minutes)"""
        old_time = time.time() - 300  # 5 minutes ago
        result = await self.requests.delete_many({"start_time": {"$lt": old_time}})
        return result.deleted_count