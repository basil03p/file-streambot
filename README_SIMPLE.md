# 🤖 FileStreamBot - Simple Setup Guide

A Telegram bot that lets users stream and download files with automatic cleanup and multi-bot support.

## 🎯 What This Bot Does

- **Stream Files**: Users send files, bot creates streaming links
- **Auto Delete**: Files disappear after 1 hour (saves storage)
- **One Request Rule**: Users can only have one active request at a time
- **Multi-Bot Speed**: Use multiple bot tokens for faster processing
- **Channel Features**: Special features for your authorized channel

## 🚀 Quick Start (5 Minutes)

### Step 1: Get Your Bot Ready
1. Message [@BotFather](https://t.me/BotFather) on Telegram
2. Type `/newbot` and follow instructions
3. Save your bot token (looks like: `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`)

### Step 2: Get Telegram API Credentials
1. Go to [my.telegram.org](https://my.telegram.org)
2. Login with your phone number
3. Click "API Development Tools"
4. Create an app and save your `API_ID` and `API_HASH`

### Step 3: Download and Setup
```bash
# Download the bot
git clone https://github.com/basil03p/FileStreamBot
cd FileStreamBot

# Install requirements
pip install -r requirements.txt
```

### Step 4: Create Environment File
Create a file called `.env` with these settings:

```env
# Your Telegram API credentials (required)
API_ID=12345678
API_HASH=your_api_hash_here
BOT_TOKEN=your_bot_token_here

# Your Telegram user ID (required)
OWNER_ID=your_telegram_user_id

# Database (required)
DATABASE_URL=mongodb://localhost:27017

# Log channels (optional but recommended)
FLOG_CHANNEL=-1001234567890
ULOG_CHANNEL=-1001234567890
```

### Step 5: Run Your Bot
```bash
python -m FileStream
```

That's it! Your bot is running with basic features.

## 🔥 Add Speed Boost (Optional)

Want your bot to be super fast? Add helper bots:

### Step 1: Create Helper Bots
1. Go back to [@BotFather](https://t.me/BotFather)
2. Create 2-3 more bots using `/newbot`
3. Save all the bot tokens

### Step 2: Add Tokens to Your .env File
```env
# Enable multi-bot mode
MULTI_BOT_MODE=true

# Add your helper bot tokens
MULTITOKEN1=helper_bot_token_1
MULTITOKEN2=helper_bot_token_2
MULTITOKEN3=helper_bot_token_3
```

### Step 3: Restart Your Bot
```bash
# Stop the bot (Ctrl+C) then restart
python -m FileStream
```

Now your bot uses multiple bots for faster file processing!

## 🎁 Special Channel Features (Optional)

Want special features for your channel? Set this up:

```env
# Your channel ID (get it from @userinfobot)
AUTH_CHANNEL=-1001234567890

# Enable download links for channel files
GENERATE_DOWNLOAD_LINKS=true
```

## 📱 How Users Use Your Bot

1. **Send File**: User sends any file to your bot
2. **Get Links**: Bot responds with streaming/download links
3. **Auto Cleanup**: File gets deleted after 1 hour automatically
4. **One at a Time**: Users can only have one active request

### User Commands
- `/start` - Start the bot
- `/help` - Get help
- `/revoke` - Cancel current request
- `/status` - Check request status

## 🔧 Common Problems & Solutions

### Problem: "Module not found"
**Solution**: Install requirements
```bash
pip install -r requirements.txt
```

### Problem: "Database connection failed"
**Solution**: Install and start MongoDB
```bash
# Windows (using chocolatey)
choco install mongodb

# Or use MongoDB Atlas (cloud) and put the connection string in DATABASE_URL
```

### Problem: "Bot doesn't respond"
**Solution**: Check your bot token and API credentials

### Problem: "Files not deleting automatically"
**Solution**: The bot has background cleanup running every 5 minutes. Check logs for any errors.

## 🌟 Understanding the Features

### 🕐 1-Hour Auto Delete
- Saves your server storage
- Files automatically disappear after 1 hour
- Users get warning when time is running out

### 🚫 One Request Rule
- Prevents spam and server overload
- Users must wait for current request to finish
- Can cancel anytime with `/revoke`

### ⚡ Multi-Bot System
- Main bot talks to users
- Helper bots process files in background
- Much faster than single bot
- Automatic load balancing

## 📊 Owner Commands

As the bot owner, you get special commands:

- `/botstats` - See multi-bot statistics
- `/broadcast <message>` - Send message to all users
- `/ban <user_id>` - Ban a user
- `/unban <user_id>` - Unban a user

## 🔒 Security Features

- Only owner can use admin commands
- User request tracking and limits
- Automatic cleanup prevents storage abuse
- Optional force subscribe to your channel

## 📝 Quick Troubleshooting

### Check if everything is working:
```bash
# Check if bot is running
python -c "print('Bot should be running...')"

# Check environment variables
python -c "import os; print('API_ID:', os.getenv('API_ID'))"
```

### View bot logs:
```bash
# Check the log file for errors
tail -f streambot.log
```

## 🎉 Your Bot is Ready!

1. Start with basic setup
2. Add multi-bot speed boost when needed
3. Configure channel features if you have a channel
4. Monitor with owner commands

For detailed technical documentation, see the main `README.md` file.

---

Need help? Create an issue on GitHub or check the logs! 🚀
