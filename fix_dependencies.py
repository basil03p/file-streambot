#!/usr/bin/env python3
"""
FileStreamBot Dependency Fix Script
Handles compatibility issues between motor and pymongo versions
"""

import sys
import subprocess
import pkg_resources

def install_compatible_versions():
    """Install compatible versions of motor and pymongo"""
    
    # Compatible version combinations
    compatible_packages = [
        "motor==3.5.1",
        "pymongo==4.8.0",
        "dnspython==2.4.2"
    ]
    
    print("🔧 Installing compatible MongoDB drivers...")
    
    for package in compatible_packages:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--upgrade"])
            print(f"✅ Installed {package}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install {package}: {e}")
            return False
    
    return True

def verify_imports():
    """Verify that all required modules can be imported"""
    
    test_imports = [
        ("motor.motor_asyncio", "MongoDB async driver"),
        ("pymongo", "MongoDB driver"),
        ("bson.objectid", "BSON ObjectId"),
        ("aiohttp", "Async HTTP client"),
        ("pyrofork", "Telegram client")
    ]
    
    print("\n🧪 Testing imports...")
    
    all_good = True
    for module_name, description in test_imports:
        try:
            __import__(module_name)
            print(f"✅ {description} ({module_name})")
        except ImportError as e:
            print(f"❌ {description} ({module_name}): {e}")
            all_good = False
    
    return all_good

if __name__ == "__main__":
    print("FileStreamBot Dependency Fix Script")
    print("=" * 40)
    
    # Install compatible versions
    if install_compatible_versions():
        print("\n✅ Package installation completed")
    else:
        print("\n❌ Package installation failed")
        sys.exit(1)
    
    # Verify imports
    if verify_imports():
        print("\n🎉 All dependencies are working correctly!")
        print("You can now run: python -m FileStream")
    else:
        print("\n❌ Some imports are still failing")
        print("Try running this script again or check the logs")
        sys.exit(1)
