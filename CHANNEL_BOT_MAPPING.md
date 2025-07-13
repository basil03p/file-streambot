# Channel-Bot Mapping Configuration

## Overview
The bot now uses different bot instances for different types of channels based on admin permissions:

## Channel Types & Bot Assignment

### 🗂️ **FLOG_CHANNEL** (File Logs)
- **Bot Used**: Multi-bot clients (any available processing bot)
- **Purpose**: Store uploaded files and file metadata
- **Required Permissions**: 
  - ✅ Post Messages
  - ✅ Edit Messages  
  - ✅ Delete Messages
- **Admin Requirement**: All multi-bots must be admin

### 👥 **ULOG_CHANNEL** (User Activity Logs)
- **Bot Used**: Main bot only (`FileStream`)
- **Purpose**: Log user activities, new users, flood waits, errors
- **Required Permissions**:
  - ✅ Post Messages
- **Admin Requirement**: Only main bot needs admin access

### 📢 **FORCE_SUB_ID** (Force Subscribe Channel)
- **Bot Used**: Main bot only
- **Purpose**: Check user subscription status
- **Required Permissions**:
  - ✅ View Channel (to check membership)
- **Admin Requirement**: Main bot needs at least member access

### 🔐 **AUTH_CHANNEL** (Enhanced Features)
- **Bot Used**: Multi-bot clients for file operations, main bot for logs
- **Purpose**: Special channel with enhanced download features
- **Required Permissions**: Same as FLOG_CHANNEL
- **Admin Requirement**: All multi-bots must be admin

## Current Configuration (.env)

```env
# Files are stored here (multi-bots handle this)
FLOG_CHANNEL=-1002531606586

# User activity logs (main bot only)
ULOG_CHANNEL=-1002531606586

# Force subscribe channel (main bot checks membership)
FORCE_SUB_ID=-1002036635078

# Enhanced features channel (multi-bots + main bot)
AUTH_CHANNEL=-1002036635078
```

## Permission Setup Required

### For FLOG_CHANNEL (-1002531606586):
1. Add **main bot** as admin with: Post, Edit, Delete Messages
2. Add **all helper bots** (MULTI_TOKEN1, MULTI_TOKEN2, etc.) as admin with: Post, Edit, Delete Messages

### For ULOG_CHANNEL (-1002531606586):
1. Add **main bot only** as admin with: Post Messages
2. Helper bots don't need access (they won't send to this channel)

### For FORCE_SUB_ID (-1002036635078):
1. Add **main bot** as admin or member (to check subscriptions)

### For AUTH_CHANNEL (-1002036635078):
1. Add **main bot** as admin with: Post, Edit, Delete Messages
2. Add **all helper bots** as admin with: Post, Edit, Delete Messages

## How It Works

1. **File Upload Flow**:
   - User uploads file → Any available multi-bot processes it
   - File stored in FLOG_CHANNEL → Multi-bot sends file
   - User activity logged to ULOG_CHANNEL → Main bot sends log

2. **Error Handling**:
   - All errors and flood waits → Logged to ULOG_CHANNEL by main bot
   - File operation errors → Handled by the processing bot

3. **User Management**:
   - New user detection → Main bot logs to ULOG_CHANNEL
   - Subscription checks → Main bot checks FORCE_SUB_ID

## Benefits

- ✅ **Scalability**: File operations distributed across multiple bots
- ✅ **Reliability**: User logs centralized through main bot
- ✅ **Permissions**: Minimal admin requirements for user activity channel
- ✅ **Maintenance**: Clear separation of responsibilities

## Troubleshooting

If you see "Can't Edit Broadcast Message" errors:
1. Check that all multi-bots are admin in FLOG_CHANNEL
2. Verify main bot is admin in ULOG_CHANNEL
3. Ensure proper permissions are granted (Post/Edit/Delete for file channels)

The permission error you were getting was likely because multi-bots were trying to send to ULOG_CHANNEL without having admin access. Now only the main bot sends to ULOG_CHANNEL.
