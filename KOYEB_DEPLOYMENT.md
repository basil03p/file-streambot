# Koyeb Deployment Guide for FileStreamBot

## Pre-deployment Checklist

### 1. Environment Variables to Set in Koyeb:
```
API_ID=your_api_id
API_HASH=your_api_hash
BOT_TOKEN=your_bot_token
OWNER_ID=your_owner_id
DATABASE_URL=your_mongodb_connection_string
WORKERS=8
SLEEP_THRESHOLD=30
```

### 2. Optional Multi-Client Setup:
```
MULTI_TOKEN1=additional_bot_token_1
MULTI_TOKEN2=additional_bot_token_2
```

### 3. Performance Optimizations Applied:
- ✅ Fixed "min() arg is empty" error with proper fallback
- ✅ Removed Flask port conflict (uses only aiohttp)
- ✅ Increased chunk size to 2MB for faster downloads
- ✅ Added proper caching headers
- ✅ Optimized Docker image with slim base
- ✅ Added health check endpoint at /health
- ✅ Memory-optimized file caching
- ✅ Reduced sleep threshold for faster response

### 4. Koyeb-Specific Fixes:
- ✅ Dynamic port binding (uses PORT env var)
- ✅ Proper signal handling for graceful shutdown
- ✅ Optimized logging for cloud deployment
- ✅ Health check endpoint for service monitoring
- ✅ Reduced log file size to prevent storage issues

### 5. Maximum Download Speed Optimizations:
- ✅ 2MB chunk size (double the original)
- ✅ Multiple concurrent transmissions per client
- ✅ Keep-alive connections
- ✅ Proper cache headers (24-hour cache)
- ✅ ETag support for efficient caching
- ✅ Optimized client selection algorithm

### 6. Memory Management:
- ✅ Limited cache size (100 items max)
- ✅ Automatic cache cleanup every 15 minutes
- ✅ FIFO cache eviction strategy
- ✅ Reduced logging verbosity in production

## Deployment Steps:

1. **Fork this repository** to your GitHub account
2. **Set up MongoDB** (MongoDB Atlas recommended)
3. **Create a Koyeb account** and connect your GitHub
4. **Create new Koyeb service** from your forked repository
5. **Set environment variables** in Koyeb dashboard
6. **Deploy** and monitor logs for any issues

## Monitoring:
- Health check: `https://your-app.koyeb.app/health`
- Status endpoint: `https://your-app.koyeb.app/status`
- Home: `https://your-app.koyeb.app/`

## Troubleshooting:
- If clients fail to start, check API_ID and API_HASH
- If downloads are slow, verify MULTI_TOKEN setup
- If service restarts, check memory usage and logs
- If getting 503 errors, verify database connection

## Performance Tips:
- Use multiple bot tokens for better speed
- Keep bot tokens active (use them regularly)
- Monitor resource usage in Koyeb dashboard
- Enable MongoDB connection pooling
