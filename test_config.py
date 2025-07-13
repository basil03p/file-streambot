#!/usr/bin/env python3
"""
Multi-Bot Configuration Test
This script verifies the multi-bot system configuration and setup.
"""

import os
import sys
import asyncio
import logging
from FileStream.config import Telegram

async def test_configuration():
    """Test multi-bot configuration"""
    print("=" * 60)
    print("🤖 FILESTREAM BOT - MULTI-BOT CONFIGURATION TEST")
    print("=" * 60)
    
    # Test basic configuration
    print("\n📋 BASIC CONFIGURATION:")
    print(f"  ✓ Database URL: {'✓ Configured' if Telegram.DATABASE_URL else '❌ Missing'}")
    print(f"  ✓ Main Bot Token: {'✓ Configured' if Telegram.BOT_TOKEN else '❌ Missing'}")
    print(f"  ✓ API ID: {'✓ Configured' if Telegram.API_ID else '❌ Missing'}")
    print(f"  ✓ API Hash: {'✓ Configured' if Telegram.API_HASH else '❌ Missing'}")
    
    # Test multi-bot configuration
    print("\n🔄 MULTI-BOT CONFIGURATION:")
    print(f"  ✓ Multi-Bot Mode: {'✅ Enabled' if Telegram.MULTI_BOT_MODE else '❌ Disabled'}")
    
    if Telegram.MULTI_BOT_MODE:
        if Telegram.MULTI_TOKENS:
            print(f"  ✓ Backend Tokens: ✅ {len(Telegram.MULTI_TOKENS)} tokens configured")
            for i, token in enumerate(Telegram.MULTI_TOKENS, 1):
                masked_token = f"{token[:8]}...{token[-8:]}" if len(token) > 16 else "Invalid"
                print(f"    - Backend Bot {i}: {masked_token}")
        else:
            print("  ❌ Backend Tokens: Missing! Add MULTI_TOKENS environment variable")
    
    # Test optional features
    print("\n⚡ OPTIONAL FEATURES:")
    print(f"  ✓ Auth Channel: {'✅ ' + str(Telegram.AUTH_CHANNEL) if Telegram.AUTH_CHANNEL else '❌ Not configured'}")
    print(f"  ✓ Download Links: {'✅ Enabled' if Telegram.GENERATE_DOWNLOAD_LINKS else '❌ Disabled'}")
    print(f"  ✓ Force Subscribe: {'✅ Enabled' if Telegram.FORCE_SUB else '❌ Disabled'}")
    
    # Test server configuration
    print("\n🌐 SERVER CONFIGURATION:")
    from FileStream.config import Server
    print(f"  ✓ Server URL: {Server.URL}")
    print(f"  ✓ Bind Address: {Server.BIND_ADDRESS}")
    print(f"  ✓ Port: {Server.PORT}")
    
    # Architecture summary
    print("\n🏗️ ARCHITECTURE SUMMARY:")
    if Telegram.MULTI_BOT_MODE and Telegram.MULTI_TOKENS:
        print("  ✅ Multi-Bot Architecture Active")
        print(f"  📱 Main Bot: Handles ALL user interactions")
        print(f"  ⚙️ Backend Bots: {len(Telegram.MULTI_TOKENS)} bots for processing")
        print("  🚀 Performance: Speed boost enabled for file processing")
    else:
        print("  📱 Single Bot Mode: Main bot handles everything")
        print("  💡 Tip: Enable multi-bot mode for better performance")
    
    print("\n" + "=" * 60)
    print("✅ Configuration test completed!")
    print("=" * 60)

if __name__ == "__main__":
    try:
        asyncio.run(test_configuration())
    except Exception as e:
        print(f"❌ Error during configuration test: {e}")
        sys.exit(1)
