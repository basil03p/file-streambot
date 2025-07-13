# File Management System Update

## New Features

### 1. Automatic File Expiration (1 Hour)
- All uploaded files are automatically deleted from the database after 1 hour
- Files include an expiration timestamp and remaining time display
- Background cleanup tasks run every 5 minutes to remove expired files
- Web interface shows remaining time for each file
- Expired files are automatically cleaned up when accessed

### 2. One Request at a Time Limitation
- Users can only process one file upload at a time
- If a user tries to upload while having an active request, they receive a warning message
- Active requests have a 5-minute timeout to prevent stuck requests
- Background cleanup removes old active requests every minute

## Implementation Details

### Database Changes
- Added `expires_at` field to file documents (timestamp)
- Added `active_requests` collection to track user requests
- Enhanced cleanup methods for expired files and old requests

### Background Tasks
- File cleanup task runs every 5 minutes
- Request cleanup task runs every 1 minute
- Automatic startup and shutdown with the main application

### User Experience
- Processing message shown during file upload
- Clear error messages for multiple requests
- Expiration time displayed in:
  - Bot messages
  - Web download pages
  - Video player pages

### Migration
- Run `migrate_files.py` once to add expiration times to existing files
- Existing files get 1-hour expiration from their creation time
- Already expired files get 1-minute grace period

## Configuration

No additional configuration required. The system uses:
- 1 hour (3600 seconds) file expiration
- 5 minutes (300 seconds) cleanup interval for files
- 1 minute (60 seconds) cleanup interval for requests
- 5 minutes (300 seconds) request timeout

## Files Modified

### Core Files
- `FileStream/utils/database.py` - Added expiration and request tracking methods
- `FileStream/utils/background_tasks.py` - New background task system
- `FileStream/__main__.py` - Integrated background tasks
- `FileStream/bot/plugins/stream.py` - Added request limiting
- `FileStream/bot/plugins/start.py` - Added expiration checks
- `FileStream/utils/bot_utils.py` - Added expiration time display
- `FileStream/utils/file_properties.py` - Added expiration validation
- `FileStream/utils/render_template.py` - Added web expiration handling

### Templates
- `FileStream/template/dl.html` - Added expiration time display
- `FileStream/template/play.html` - Added expiration time display

### Migration
- `migrate_files.py` - One-time migration script for existing files

## Usage Notes

1. **For New Deployments**: No additional setup required
2. **For Existing Deployments**: Run the migration script once:
   ```bash
   python migrate_files.py
   ```
3. **Monitoring**: Check logs for cleanup activities and request limiting
4. **Database**: Ensure MongoDB supports the new collections and fields

## Benefits

- **Storage Efficiency**: Automatic cleanup prevents database bloat
- **User Management**: Request limiting prevents spam and abuse
- **Transparency**: Users see exactly when their files will expire
- **Reliability**: Background tasks ensure system stays clean
- **Performance**: Regular cleanup maintains optimal database performance
