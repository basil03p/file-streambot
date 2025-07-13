#!/bin/bash
# FileStreamBot Startup Script
# Handles dependency issues and starts the bot

echo "🚀 Starting FileStreamBot..."
echo "📋 Checking dependencies..."

# Fix potential motor/pymongo compatibility
python3 -c "
try:
    import motor.motor_asyncio
    import pymongo
    print('✅ MongoDB drivers OK')
except ImportError as e:
    print(f'❌ MongoDB driver issue: {e}')
    print('🔧 Installing compatible versions...')
    import subprocess
    import sys
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'motor==3.5.1', 'pymongo==4.8.0', '--upgrade'])
    print('✅ Fixed MongoDB drivers')
"

# Check all critical imports
python3 -c "
import sys
required_modules = [
    'aiohttp',
    'pyrofork', 
    'motor.motor_asyncio',
    'pymongo',
    'python_dotenv',
    'tgcrypto'
]

for module in required_modules:
    try:
        __import__(module)
        print(f'✅ {module}')
    except ImportError as e:
        print(f'❌ {module}: {e}')
        sys.exit(1)

print('🎉 All dependencies verified!')
"

# Start the bot
echo "🤖 Starting FileStreamBot..."
python3 -m FileStream
