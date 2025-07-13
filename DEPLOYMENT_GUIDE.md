# 🚀 FileStreamBot Deployment Guide

Complete guide for deploying FileStreamBot on various platforms.

## 📋 Prerequisites

Before deploying anywhere, make sure you have:

✅ Telegram Bot Token(s) from [@BotFather](https://t.me/BotFather)  
✅ Telegram API credentials from [my.telegram.org](https://my.telegram.org)  
✅ Your Telegram User ID (get from [@userinfobot](https://t.me/userinfobot))  
✅ MongoDB database (local or cloud)  

## 🏠 Local Development

### Windows
```powershell
# Clone repository
git clone https://github.com/basil03p/FileStreamBot
cd FileStreamBot

# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Create .env file (see configuration section)
# Run the bot
python -m FileStream
```

### Linux/macOS
```bash
# Clone repository
git clone https://github.com/basil03p/FileStreamBot
cd FileStreamBot

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file (see configuration section)
# Run the bot
python -m FileStream
```

## ☁️ Cloud Platforms

### 1. Heroku (Free Tier Available)

**Step 1**: Prepare for Heroku
```bash
# Install Heroku CLI
# Windows: Download from heroku.com
# Linux: curl https://cli-assets.heroku.com/install.sh | sh
# macOS: brew tap heroku/brew && brew install heroku

# Login to Heroku
heroku login
```

**Step 2**: Create Heroku App
```bash
# In your project directory
heroku create your-filestream-bot

# Add MongoDB addon (optional)
heroku addons:create mongolab:sandbox

# Or use MongoDB Atlas (recommended)
```

**Step 3**: Configure Environment Variables
```bash
heroku config:set API_ID=your_api_id
heroku config:set API_HASH=your_api_hash
heroku config:set BOT_TOKEN=your_bot_token
heroku config:set OWNER_ID=your_user_id
heroku config:set DATABASE_URL=your_mongodb_url

# Optional: Multi-bot setup
heroku config:set MULTI_BOT_MODE=true
heroku config:set MULTITOKEN1=helper_bot_token_1
heroku config:set MULTITOKEN2=helper_bot_token_2
```

**Step 4**: Deploy
```bash
git add .
git commit -m "Deploy FileStreamBot"
git push heroku main
```

### 2. Railway (Modern Platform)

**Step 1**: Setup Railway
1. Visit [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"

**Step 2**: Configure Variables
Add these environment variables in Railway dashboard:
```
API_ID=your_api_id
API_HASH=your_api_hash
BOT_TOKEN=your_bot_token
OWNER_ID=your_user_id
DATABASE_URL=your_mongodb_url
```

**Step 3**: Deploy
Railway automatically deploys when you push to GitHub!

### 3. Render (Free Tier)

**Step 1**: Create Web Service
1. Go to [render.com](https://render.com)
2. Connect your GitHub repository
3. Create new "Web Service"

**Step 2**: Configuration
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python -m FileStream`
- **Environment**: Python 3

**Step 3**: Environment Variables
Add your environment variables in Render dashboard.

### 4. Koyeb (Global Edge)

See `KOYEB_DEPLOYMENT.md` for detailed Koyeb deployment instructions.

## 🐳 Docker Deployment

### Docker Compose (Recommended)

**Step 1**: Create `docker-compose.yml`
```yaml
version: '3.8'

services:
  filestream:
    build: .
    restart: unless-stopped
    environment:
      - API_ID=${API_ID}
      - API_HASH=${API_HASH}
      - BOT_TOKEN=${BOT_TOKEN}
      - OWNER_ID=${OWNER_ID}
      - DATABASE_URL=mongodb://mongo:27017/filestream
      - MULTI_BOT_MODE=${MULTI_BOT_MODE:-false}
      - MULTITOKEN1=${MULTITOKEN1}
      - MULTITOKEN2=${MULTITOKEN2}
      - MULTITOKEN3=${MULTITOKEN3}
    ports:
      - "8080:8080"
    depends_on:
      - mongo
    volumes:
      - ./downloads:/app/downloads

  mongo:
    image: mongo:5.0
    restart: unless-stopped
    volumes:
      - mongodb_data:/data/db
    environment:
      MONGO_INITDB_DATABASE: filestream

volumes:
  mongodb_data:
```

**Step 2**: Create `.env` file
```env
API_ID=your_api_id
API_HASH=your_api_hash
BOT_TOKEN=your_bot_token
OWNER_ID=your_user_id
MULTI_BOT_MODE=true
MULTITOKEN1=helper_token_1
MULTITOKEN2=helper_token_2
MULTITOKEN3=helper_token_3
```

**Step 3**: Deploy
```bash
docker-compose up -d
```

### Single Docker Container

**Step 1**: Build Image
```bash
docker build -t filestream-bot .
```

**Step 2**: Run Container
```bash
docker run -d \
  --name filestream-bot \
  -p 8080:8080 \
  -e API_ID=your_api_id \
  -e API_HASH=your_api_hash \
  -e BOT_TOKEN=your_bot_token \
  -e OWNER_ID=your_user_id \
  -e DATABASE_URL=your_mongodb_url \
  filestream-bot
```

## 🖥️ VPS/Server Deployment

### Ubuntu/Debian Server

**Step 1**: Update System
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-pip python3-venv git -y
```

**Step 2**: Install MongoDB
```bash
# Install MongoDB
wget -qO - https://www.mongodb.org/static/pgp/server-5.0.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/5.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-5.0.list
sudo apt update
sudo apt install -y mongodb-org

# Start MongoDB
sudo systemctl start mongod
sudo systemctl enable mongod
```

**Step 3**: Setup Application
```bash
# Clone and setup
git clone https://github.com/basil03p/FileStreamBot
cd FileStreamBot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create environment file
nano .env
# Add your configuration here
```

**Step 4**: Create Systemd Service
```bash
sudo nano /etc/systemd/system/filestream.service
```

Add this content:
```ini
[Unit]
Description=FileStream Bot
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/FileStreamBot
Environment=PATH=/home/ubuntu/FileStreamBot/venv/bin
ExecStart=/home/ubuntu/FileStreamBot/venv/bin/python -m FileStream
Restart=always

[Install]
WantedBy=multi-user.target
```

**Step 5**: Start Service
```bash
sudo systemctl daemon-reload
sudo systemctl enable filestream
sudo systemctl start filestream

# Check status
sudo systemctl status filestream
```

### CentOS/RHEL Server

**Step 1**: Update System
```bash
sudo yum update -y
sudo yum install python3 python3-pip git -y
```

**Step 2**: Install MongoDB
```bash
# Create MongoDB repo file
sudo tee /etc/yum.repos.d/mongodb-org-5.0.repo <<EOF
[mongodb-org-5.0]
name=MongoDB Repository
baseurl=https://repo.mongodb.org/yum/redhat/8/mongodb-org/5.0/x86_64/
gpgcheck=1
enabled=1
gpgkey=https://www.mongodb.org/static/pgp/server-5.0.asc
EOF

# Install MongoDB
sudo yum install -y mongodb-org

# Start MongoDB
sudo systemctl start mongod
sudo systemctl enable mongod
```

Follow the same steps as Ubuntu for application setup.

## 🗄️ Database Options

### Option 1: MongoDB Atlas (Cloud - Recommended)
1. Go to [mongodb.com/atlas](https://mongodb.com/atlas)
2. Create free account
3. Create cluster (free tier: 512MB)
4. Get connection string
5. Use in `DATABASE_URL`

### Option 2: Local MongoDB
```bash
# Install MongoDB locally
# Use DATABASE_URL=mongodb://localhost:27017/filestream
```

### Option 3: Docker MongoDB
```bash
docker run -d \
  --name mongodb \
  -p 27017:27017 \
  -v mongodb_data:/data/db \
  mongo:5.0
```

## ⚙️ Environment Configuration

### Basic Configuration (.env file)
```env
# Required
API_ID=12345678
API_HASH=abcdef1234567890abcdef1234567890
BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrSTUvwxyz
OWNER_ID=123456789
DATABASE_URL=mongodb://localhost:27017/filestream

# Optional
MULTI_BOT_MODE=true
MULTITOKEN1=helper_bot_token_1
MULTITOKEN2=helper_bot_token_2
MULTITOKEN3=helper_bot_token_3

# Channel Features
AUTH_CHANNEL=-1001234567890
GENERATE_DOWNLOAD_LINKS=true

# Logging
FLOG_CHANNEL=-1001234567890
ULOG_CHANNEL=-1001234567890

# Server
PORT=8080
BIND_ADDRESS=0.0.0.0
```

### Production Configuration
```env
# All basic configs plus:

# Security
HAS_SSL=true
FQDN=yourdomain.com

# Performance
WORKERS=4
MAX_REQUESTS=1000

# Features
FORCE_SUB_ID=-1001234567890
FORCE_UPDATES_CHANNEL=true
NO_PORT=true
```

## 🔍 Monitoring & Maintenance

### Check Bot Status
```bash
# Check logs
tail -f streambot.log

# Check process
ps aux | grep python

# Check MongoDB
mongo --eval "db.stats()"
```

### Update Bot
```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install -r requirements.txt

# Restart service
sudo systemctl restart filestream
```

### Backup Database
```bash
# MongoDB backup
mongodump --db filestream --out backup/

# Restore
mongorestore backup/
```

## 🚨 Troubleshooting

### Common Issues

1. **Bot not responding**
   - Check bot token
   - Verify API credentials
   - Check internet connection

2. **Database connection failed**
   - Verify MongoDB is running
   - Check connection string
   - Verify network access

3. **Files not processing**
   - Check disk space
   - Verify permissions
   - Check helper bot tokens

4. **Memory issues**
   - Monitor RAM usage
   - Adjust worker count
   - Check for memory leaks

### Debug Commands
```bash
# Check environment variables
env | grep -E "(API_|BOT_|DATABASE_)"

# Test database connection
python -c "from FileStream.utils.database import Database; print('DB OK')"

# Check bot connection
python -c "from pyrogram import Client; print('Pyrogram OK')"
```

## 📊 Performance Tips

### Optimization
- Use SSD storage for better I/O
- Enable multi-bot mode for higher throughput
- Monitor resource usage regularly
- Set up proper logging

### Scaling
- Add more helper bots as needed
- Use load balancer for multiple instances
- Implement caching for frequent requests
- Monitor and upgrade server resources

## 🔐 Security Best Practices

1. **Environment Variables**
   - Never commit `.env` files
   - Use secure environment variable storage
   - Rotate bot tokens periodically

2. **Server Security**
   - Keep system updated
   - Use firewall rules
   - Enable SSL/HTTPS
   - Regular security audits

3. **Bot Security**
   - Limit owner commands
   - Implement rate limiting
   - Monitor unusual activity
   - Regular backups

## 📞 Support

If you need help with deployment:

1. Check the logs first
2. Verify your configuration
3. Test with minimal setup
4. Create GitHub issue with details

---

**Happy Deploying! 🚀**
