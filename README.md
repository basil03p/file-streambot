# 🚀 Enhanced FileStreamBot

A powerful Telegram bot for streaming and downloading files with advanced features including multi-bot support, auto-expiration, and request management.

## ✨ Features

### 🎯 Core Features
- **File Streaming**: Direct streaming of videos and media files
- **Download Links**: Generate download links for any file type
- **Auto-Expiration**: Files automatically deleted after 1 hour
- **Request Management**: One request at a time per user with revocation support
- **Channel Support**: Enhanced features for authorized channels

### ⚡ Advanced Features
- **Multi-Bot System**: Use multiple bot tokens for speed boost
- **Load Balancing**: Intelligent distribution across bot instances
- **Background Cleanup**: Automatic cleanup of expired files and requests
- **Enhanced UI**: Special buttons and options for auth channel files
- **Real-time Status**: Track request progress and remaining time

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- MongoDB database
- Telegram bot tokens (main + optional helper bots)
- Telegram API credentials

### 1. Clone Repository
```bash
git clone https://github.com/basil03p/FileStreamBot
cd FileStreamBot
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Setup
Create a `.env` file with the following variables:

#### Required Variables
```env
# Telegram API Credentials
API_ID=your_telegram_api_id
API_HASH=your_telegram_api_hash

# Main Bot Token
BOT_TOKEN=your_main_bot_token

# Database
DATABASE_URL=mongodb://localhost:27017

# Bot Owner
OWNER_ID=your_telegram_user_id

# Log Channels
FLOG_CHANNEL=-1001234567890  # For file logs
ULOG_CHANNEL=-1001234567890  # For user logs

# Optional: Force Subscribe
FORCE_SUB_ID=-1001234567890  # Channel users must join
FORCE_UPDATES_CHANNEL=true
```

#### Multi-Bot Configuration (Optional)
```env
# Enable Multi-Bot Mode
MULTI_BOT_MODE=true

# Authorized Channel (gets enhanced features)
AUTH_CHANNEL=-1001234567890

# Enable download links for auth channel
GENERATE_DOWNLOAD_LINKS=true

# Helper Bot Tokens (for speed boost)
MULTITOKEN1=bot_token_1
MULTITOKEN2=bot_token_2
MULTITOKEN3=bot_token_3
# ... up to MULTITOKEN10
```

#### Server Configuration (Optional)
```env
# Web Server
PORT=8080
BIND_ADDRESS=0.0.0.0

# SSL (if using HTTPS)
HAS_SSL=false
NO_PORT=false
FQDN=your-domain.com
```

### 4. Run the Bot
```bash
python -m FileStream
```

## 🔧 Configuration Guide

### Setting Up Multiple Bots

1. **Create Helper Bots**:
   - Go to [@BotFather](https://t.me/BotFather)
   - Create new bots using `/newbot`
   - Get bot tokens for each helper bot

2. **Add Bot Tokens**:
   ```env
   MULTITOKEN1=1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghi
   MULTITOKEN2=1234567891:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghi
   MULTITOKEN3=1234567892:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghi
   ```

3. **Enable Multi-Bot Mode**:
   ```env
   MULTI_BOT_MODE=true
   ```

### Setting Up Auth Channel

1. **Create/Configure Channel**:
   - Create a Telegram channel
   - Add your main bot as admin
   - Add helper bots as admins (for download support)

2. **Set Channel ID**:
   ```env
   AUTH_CHANNEL=-1001234567890  # Your channel ID
   GENERATE_DOWNLOAD_LINKS=true
   ```

## 🎮 Bot Commands

### 👤 User Commands
| Command | Description |
|---------|-------------|
| `/start` | Start the bot and get welcome message |
| `/help` | Get help and command list |
| `/files` | View your uploaded files |
| `/revoke` | Cancel your active file request |
| `/status` | Check your request status |
| `/about` | Bot information and version |

### 👑 Owner Commands
| Command | Description |
|---------|-------------|
| `/botstats` | Multi-bot system statistics |
| `/status` | Overall bot status |
| `/ban <user_id>` | Ban a user |
| `/unban <user_id>` | Unban a user |
| `/broadcast` | Broadcast message to all users |
| `/del <file_id>` | Delete a specific file |

## 🔄 How It Works

### 📤 File Upload Process
1. **User sends file** to the main bot
2. **Request validation** - Check for active requests
3. **Bot selection** - Choose helper bot for processing (if enabled)
4. **File processing** - Generate download links
5. **Response** - Send links with expiration timer
6. **Auto-cleanup** - File expires after 1 hour

### 🏃 Multi-Bot Speed Boost
- **Main Bot**: Handles all user interactions, commands, and file reception
- **Helper Bots**: Used for backend file processing and streaming
- **Load Balancing**: Requests distributed across available helper bots
- **Fallback**: If helper bots fail, main bot handles everything

### 📺 Channel Integration
Files from authorized channels get:
- **Enhanced UI** with multiple download options
- **Direct download links** alongside streaming
- **Priority processing** with dedicated bot assignment
- **Special button layouts** for better user experience

## 🎛️ Advanced Features

### ⏰ Auto-Expiration System
- Files automatically expire after **1 hour**
- **Background cleanup** runs every 5 minutes
- **User notification** shows remaining time
- **Graceful handling** of expired file access

### 🔒 Request Management
- **One request at a time** per user
- **Request tracking** with detailed status
- **User control** - cancel requests anytime
- **Timeout protection** - 5-minute automatic cleanup

### 📊 Monitoring & Logs
- **Real-time statistics** for multi-bot performance
- **Request tracking** with timestamps and status
- **Error handling** with comprehensive logging
- **Performance metrics** for optimization

## 🐳 Docker Deployment

### Docker Compose
```yaml
version: '3.8'
services:
  filestream:
    build: .
    environment:
      - API_ID=your_api_id
      - API_HASH=your_api_hash
      - BOT_TOKEN=your_bot_token
      - DATABASE_URL=mongodb://mongo:27017
      - MULTI_BOT_MODE=true
      - MULTITOKEN1=helper_bot_token_1
    ports:
      - "8080:8080"
    depends_on:
      - mongo
    
  mongo:
    image: mongo:latest
    volumes:
      - mongodb_data:/data/db

volumes:
  mongodb_data:
```

### Run with Docker
```bash
docker-compose up -d
```

## ☁️ Cloud Deployment

### Heroku
1. Fork this repository
2. Create new Heroku app
3. Connect GitHub repository
4. Set environment variables in Heroku dashboard
5. Deploy from GitHub

### Railway
1. Connect your GitHub repository
2. Add environment variables
3. Deploy automatically

### VPS/Server
1. Clone repository on server
2. Set up environment variables
3. Install dependencies
4. Run with systemd or PM2

## 🔧 Migration

### For Existing Installations
If you're upgrading from an older version:

1. **Database Migration**:
   ```bash
   python migrate_files.py
   ```

2. **Update Environment**:
   - Add new environment variables
   - Configure multi-bot settings if desired

3. **Restart Bot**:
   ```bash
   python -m FileStream
   ```

## 🎯 Performance Tips

### Optimization
- **Use SSD storage** for better I/O performance
- **Increase worker count** for high traffic
- **Monitor bot statistics** regularly
- **Clean up logs** periodically

### Scaling
- **Add more helper bots** for higher capacity
- **Use CDN** for better global performance
- **Implement caching** for frequently accessed files
- **Monitor resource usage** and scale accordingly

## 🐛 Troubleshooting

### Common Issues

#### Multi-Bot Not Working
```bash
# Check environment variables
echo $MULTI_BOT_MODE
echo $MULTITOKEN1

# Check bot initialization logs
tail -f streambot.log | grep "Multi-bot"
```

#### Files Not Expiring
```bash
# Check background tasks
tail -f streambot.log | grep "cleanup"

# Manual cleanup
python -c "
from FileStream.utils.database import Database
from FileStream.config import Telegram
import asyncio

async def cleanup():
    db = Database(Telegram.DATABASE_URL, Telegram.SESSION_NAME)
    count = await db.delete_expired_files()
    print(f'Cleaned up {count} files')

asyncio.run(cleanup())
"
```

#### Database Connection Issues
```bash
# Test MongoDB connection
python -c "
import pymongo
client = pymongo.MongoClient('your_database_url')
print(client.admin.command('ismaster'))
"
```

### Getting Help
- Check logs in `streambot.log`
- Use `/botstats` command for system status
- Monitor MongoDB for database issues
- Check network connectivity for Telegram API

## 📝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⭐ Support

If you find this project helpful, please give it a star ⭐

For support and updates, join our Telegram channel: [@YourChannel](https://t.me/YourChannel)

## 🔄 Changelog

### v2.0.0 (Latest)
- ✅ Multi-bot system implementation
- ✅ Auto-expiration feature (1 hour)
- ✅ Request management and revocation
- ✅ Enhanced auth channel support
- ✅ Background cleanup tasks
- ✅ Load balancing system
- ✅ Improved user interface

### v1.0.0
- ✅ Basic file streaming
- ✅ Download link generation
- ✅ Channel support
- ✅ User management

## 📚 Documentation Library

### 🚀 Quick Start Guides
- **`README_SIMPLE.md`** - 5-minute setup guide for beginners
- **`FEATURES_OVERVIEW.md`** - Complete feature list and capabilities
- **`CONFIGURATION_GUIDE.md`** - Detailed configuration reference
- **`DEPLOYMENT_GUIDE.md`** - Comprehensive deployment for all platforms

### 🔧 Technical Documentation
- **`MULTI_BOT_IMPLEMENTATION.md`** - Multi-bot system architecture
- **`FILE_MANAGEMENT_UPDATE.md`** - File expiration and cleanup system
- **`KOYEB_DEPLOYMENT.md`** - Koyeb-specific deployment guide

### 📋 Configuration Files
- **`MULTI_BOT_CONFIG.env`** - Example multi-bot configuration
- **`.env.example`** - Sample environment configuration

## 🎯 Quick Navigation

| I want to... | Check this file |
|--------------|----------------|
| **Set up quickly** | `README_SIMPLE.md` |
| **See all features** | `FEATURES_OVERVIEW.md` |
| **Deploy properly** | `DEPLOYMENT_GUIDE.md` |
| **Configure settings** | `CONFIGURATION_GUIDE.md` |
| **Understand multi-bot** | `MULTI_BOT_IMPLEMENTATION.md` |
| **Deploy on Koyeb** | `KOYEB_DEPLOYMENT.md` |

## 🌟 What Makes This Special

### 🎯 Unique Features
- **Auto-Expiring Files**: Prevents storage abuse with 1-hour expiration
- **Multi-Bot Architecture**: Speed boost using multiple bot instances
- **Request Management**: One request per user with revocation support
- **Channel Integration**: Enhanced features for authorized channels
- **Zero Maintenance**: Background cleanup handles everything automatically

### 🚀 Performance Advantages
- **5x Faster Processing**: Multi-bot system distributes load
- **Smart Load Balancing**: Intelligent bot selection for optimal performance
- **Failover Protection**: Automatic fallback if helper bots fail
- **Resource Efficient**: Automatic cleanup prevents storage bloat

### 👥 User Experience
- **Intuitive Interface**: Clean, easy-to-use buttons and commands
- **Real-Time Status**: Track request progress and remaining time
- **Error Handling**: Clear error messages and helpful guidance
- **Mobile Optimized**: Perfect experience on all devices

## ❤️ Credits & Community

### 🙏 Acknowledgments
This is an enhanced version of the original FileStreamBot with significant improvements:
- Multi-bot architecture for speed
- Auto-expiration system for storage management
- Advanced request tracking and management
- Comprehensive documentation and guides

### 🤝 Contributing
We welcome contributions! Please:
1. Fork the repository
2. Create a feature branch
3. Make your improvements
4. Submit a pull request

### 💬 Support & Community
- **GitHub Issues**: Report bugs and request features
- **Documentation**: Comprehensive guides for all skill levels
- **Community**: Share your experience and help others

---

## 🎉 Ready to Get Started?

1. **New Users**: Start with `README_SIMPLE.md` for quick setup
2. **Advanced Users**: Check `DEPLOYMENT_GUIDE.md` for production deployment
3. **Developers**: Review `MULTI_BOT_IMPLEMENTATION.md` for technical details

💡 **Need help?** Our documentation covers everything from basic setup to advanced configurations!
