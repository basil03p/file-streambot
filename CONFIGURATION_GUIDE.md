# ⚙️ FileStreamBot Configuration Guide

Complete guide to configure FileStreamBot with all available options.

## 📝 Environment Variables Reference

### 🔑 Required Variables

#### Telegram API Credentials
```env
# Get from https://my.telegram.org
API_ID=12345678
API_HASH=abcdef1234567890abcdef1234567890
```
- **API_ID**: Your Telegram API ID (integer)
- **API_HASH**: Your Telegram API Hash (32-character string)

#### Bot Configuration
```env
# Get from @BotFather
BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrSTUvwxyz

# Your Telegram User ID (get from @userinfobot)
OWNER_ID=123456789
```
- **BOT_TOKEN**: Your main bot token from BotFather
- **OWNER_ID**: Your Telegram user ID (gives you admin access)

#### Database
```env
# MongoDB connection string
DATABASE_URL=mongodb://localhost:27017/filestream

# Session name (default: StreamBot)
SESSION_NAME=StreamBot
```

### ⚡ Multi-Bot System (Optional)

```env
# Enable multi-bot mode for speed boost
MULTI_BOT_MODE=true

# Helper bot tokens (up to 10 supported)
MULTITOKEN1=123456789:ABCdefGHIjklMNOpqrSTUvwxyz
MULTITOKEN2=123456789:ABCdefGHIjklMNOpqrSTUvwxyz
MULTITOKEN3=123456789:ABCdefGHIjklMNOpqrSTUvwxyz
MULTITOKEN4=123456789:ABCdefGHIjklMNOpqrSTUvwxyz
MULTITOKEN5=123456789:ABCdefGHIjklMNOpqrSTUvwxyz
MULTITOKEN6=123456789:ABCdefGHIjklMNOpqrSTUvwxyz
MULTITOKEN7=123456789:ABCdefGHIjklMNOpqrSTUvwxyz
MULTITOKEN8=123456789:ABCdefGHIjklMNOpqrSTUvwxyz
MULTITOKEN9=123456789:ABCdefGHIjklMNOpqrSTUvwxyz
MULTITOKEN10=123456789:ABCdefGHIjklMNOpqrSTUvwxyz
```

**How Multi-Bot Works:**
- Main bot handles all user interactions
- Helper bots process files in background for speed
- Automatic load balancing across available bots
- Fallback to main bot if helpers fail

### 📺 Channel Features (Optional)

```env
# Authorized channel ID (gets special features)
AUTH_CHANNEL=-1001234567890

# Enable download links for auth channel files
GENERATE_DOWNLOAD_LINKS=true
```

**Auth Channel Benefits:**
- Enhanced UI with multiple download options
- Direct download links alongside streaming
- Priority processing with dedicated bot assignment
- Special button layouts for better UX

### 📊 Logging Channels (Optional)

```env
# Channel for file upload logs
FLOG_CHANNEL=-1001234567890

# Channel for user activity logs
ULOG_CHANNEL=-1001234567890
```

### 🔒 Force Subscribe (Optional)

```env
# Channel users must join before using bot
FORCE_SUB_ID=-1001234567890

# Enable force subscribe feature
FORCE_UPDATES_CHANNEL=true
```

### 🌐 Web Server (Optional)

```env
# Port for web server (default: 8080)
PORT=8080

# Bind address (default: 0.0.0.0)
BIND_ADDRESS=0.0.0.0

# Domain name for your bot
FQDN=yourdomain.com

# SSL configuration
HAS_SSL=false
NO_PORT=false
```

**Web Server Settings:**
- **PORT**: Port number for streaming server
- **BIND_ADDRESS**: IP address to bind (0.0.0.0 for all interfaces)
- **FQDN**: Your domain name (for URL generation)
- **HAS_SSL**: Set to true if using HTTPS
- **NO_PORT**: Set to true if using standard ports (80/443)

### 🎛️ Advanced Settings (Optional)

```env
# Maximum concurrent requests per user
MAX_USER_REQUESTS=1

# File expiration time in seconds (default: 3600 = 1 hour)
FILE_EXPIRATION_TIME=3600

# Request timeout in seconds (default: 300 = 5 minutes)
REQUEST_TIMEOUT=300

# Cleanup interval in seconds (default: 300 = 5 minutes)
CLEANUP_INTERVAL=300

# Enable debug logging
DEBUG=false

# Custom start message
CUSTOM_START_MSG="Welcome to my enhanced FileStream Bot!"

# Custom about message
CUSTOM_ABOUT_MSG="This bot is powered by FileStreamBot v2.0"
```

## 📋 Configuration Examples

### 🏠 Basic Home Setup
Perfect for personal use or testing:

```env
# Required basics
API_ID=12345678
API_HASH=your_api_hash
BOT_TOKEN=your_bot_token
OWNER_ID=your_user_id
DATABASE_URL=mongodb://localhost:27017/filestream

# Simple logging
FLOG_CHANNEL=-1001234567890
ULOG_CHANNEL=-1001234567890
```

### ⚡ High-Performance Setup
For heavy usage with multi-bot acceleration:

```env
# Required basics
API_ID=12345678
API_HASH=your_api_hash
BOT_TOKEN=your_main_bot_token
OWNER_ID=your_user_id
DATABASE_URL=mongodb://username:password@cluster.mongodb.net/filestream

# Multi-bot acceleration
MULTI_BOT_MODE=true
MULTITOKEN1=helper_bot_token_1
MULTITOKEN2=helper_bot_token_2
MULTITOKEN3=helper_bot_token_3
MULTITOKEN4=helper_bot_token_4
MULTITOKEN5=helper_bot_token_5

# Channel features
AUTH_CHANNEL=-1001234567890
GENERATE_DOWNLOAD_LINKS=true

# Logging
FLOG_CHANNEL=-1001234567890
ULOG_CHANNEL=-1001234567890

# Web server
PORT=8080
FQDN=filestream.yourdomain.com
HAS_SSL=true
NO_PORT=true
```

### 🏢 Production Server Setup
For public bots with security and monitoring:

```env
# Core configuration
API_ID=12345678
API_HASH=your_api_hash
BOT_TOKEN=your_main_bot_token
OWNER_ID=your_user_id
DATABASE_URL=mongodb+srv://user:pass@cluster.mongodb.net/filestream

# Multi-bot system
MULTI_BOT_MODE=true
MULTITOKEN1=helper_bot_token_1
MULTITOKEN2=helper_bot_token_2
MULTITOKEN3=helper_bot_token_3

# Channel configuration
AUTH_CHANNEL=-1001234567890
GENERATE_DOWNLOAD_LINKS=true
FORCE_SUB_ID=-1001234567890
FORCE_UPDATES_CHANNEL=true

# Comprehensive logging
FLOG_CHANNEL=-1001234567890
ULOG_CHANNEL=-1001234567890

# Production web server
PORT=80
BIND_ADDRESS=0.0.0.0
FQDN=bot.yourdomain.com
HAS_SSL=true
NO_PORT=true

# Performance tuning
FILE_EXPIRATION_TIME=3600
REQUEST_TIMEOUT=300
CLEANUP_INTERVAL=300
DEBUG=false
```

## 🛠️ Setup Process

### Step 1: Get Your Credentials

#### Telegram API Credentials
1. Go to [my.telegram.org](https://my.telegram.org)
2. Login with your phone number
3. Click "API development tools"
4. Create a new application
5. Note down `API_ID` and `API_HASH`

#### Bot Tokens
1. Message [@BotFather](https://t.me/BotFather)
2. Type `/newbot` for each bot you need
3. Follow the instructions
4. Save all bot tokens

#### Your User ID
1. Message [@userinfobot](https://t.me/userinfobot)
2. Note down your user ID

#### Channel IDs
1. Add [@RawDataBot](https://t.me/RawDataBot) to your channel
2. Send any message in the channel
3. Bot will show channel ID (format: -1001234567890)

### Step 2: Database Setup

#### Option A: MongoDB Atlas (Cloud)
1. Go to [mongodb.com/atlas](https://mongodb.com/atlas)
2. Create free account
3. Create cluster
4. Get connection string
5. Use format: `mongodb+srv://username:password@cluster.mongodb.net/database`

#### Option B: Local MongoDB
1. Install MongoDB on your server
2. Use format: `mongodb://localhost:27017/filestream`

### Step 3: Create Configuration File

Create `.env` file in your project root:

```bash
# Linux/macOS
nano .env

# Windows
notepad .env
```

Add your configuration based on the examples above.

### Step 4: Validate Configuration

```bash
# Test configuration
python -c "
import os
from dotenv import load_dotenv
load_dotenv()

required = ['API_ID', 'API_HASH', 'BOT_TOKEN', 'OWNER_ID', 'DATABASE_URL']
missing = [var for var in required if not os.getenv(var)]

if missing:
    print(f'Missing required variables: {missing}')
else:
    print('✅ All required variables set!')
"
```

## 🔧 Configuration Tips

### 🚀 Performance Optimization

1. **Multi-Bot Setup**
   - Use 3-5 helper bots for optimal performance
   - More bots = faster file processing
   - Each bot should be from same account

2. **Database Optimization**
   - Use MongoDB Atlas for better performance
   - Enable database indexing
   - Regular cleanup of expired data

3. **Server Configuration**
   - Use SSD storage for better I/O
   - Sufficient RAM (minimum 1GB)
   - Good internet connection

### 🔒 Security Best Practices

1. **Environment Variables**
   - Never commit `.env` files to version control
   - Use platform-specific environment variable storage
   - Rotate tokens periodically

2. **Access Control**
   - Set proper owner ID
   - Use force subscribe for public bots
   - Monitor bot usage regularly

3. **Channel Security**
   - Only add trusted channels as AUTH_CHANNEL
   - Verify channel ownership
   - Regular security audits

### 📊 Monitoring Setup

1. **Logging Channels**
   - Create dedicated channels for logs
   - Monitor file upload patterns
   - Track user activity

2. **Performance Monitoring**
   - Use `/botstats` command regularly
   - Monitor server resources
   - Track response times

## 🐛 Troubleshooting Configuration

### Common Configuration Errors

#### Invalid API Credentials
```
Error: API_ID and API_HASH invalid
```
**Solution**: Verify credentials from my.telegram.org

#### Bot Token Issues
```
Error: Bot token invalid
```
**Solution**: 
- Check token format (should be `123456789:ABC...`)
- Verify with @BotFather
- Ensure bot is not deleted

#### Database Connection
```
Error: Database connection failed
```
**Solution**:
- Test MongoDB connection
- Check network access
- Verify connection string format

#### Permission Errors
```
Error: Bot not admin in channel
```
**Solution**:
- Add bot as admin in all configured channels
- Give proper permissions (post messages, delete messages)

### Validation Commands

```bash
# Test basic configuration
python -c "
from FileStream.config import Telegram
print('API_ID:', Telegram.API_ID)
print('BOT_TOKEN:', Telegram.BOT_TOKEN[:10] + '...')
print('Database:', Telegram.DATABASE_URL.split('@')[-1] if '@' in Telegram.DATABASE_URL else Telegram.DATABASE_URL)
"

# Test database connection
python -c "
from FileStream.utils.database import Database
from FileStream.config import Telegram
import asyncio

async def test_db():
    db = Database(Telegram.DATABASE_URL, Telegram.SESSION_NAME)
    try:
        await db.total_users_count()
        print('✅ Database connection successful!')
    except Exception as e:
        print(f'❌ Database error: {e}')

asyncio.run(test_db())
"

# Test multi-bot configuration
python -c "
from FileStream.utils.multi_bot_manager import MultiBotManager
from FileStream.config import Telegram
import asyncio

async def test_multibot():
    if Telegram.MULTI_BOT_MODE:
        manager = MultiBotManager()
        await manager.initialize()
        print(f'✅ Multi-bot initialized with {len(manager.helper_bots)} helpers')
    else:
        print('ℹ️ Multi-bot mode disabled')

asyncio.run(test_multibot())
"
```

## 📚 Configuration Reference

For more specific configurations:
- See `DEPLOYMENT_GUIDE.md` for platform-specific setups
- Check `MULTI_BOT_IMPLEMENTATION.md` for multi-bot details
- Review `FILE_MANAGEMENT_UPDATE.md` for file handling options

---

**Need help?** Create an issue with your configuration details (without sensitive tokens)! 🚀
