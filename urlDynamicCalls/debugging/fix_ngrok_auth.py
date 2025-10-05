#!/usr/bin/env python3
"""
Fix ngrok authentication issues
This script helps you set up ngrok authentication properly
"""

import subprocess
import os
import sys

def check_ngrok_auth():
    """Check current ngrok authentication status"""
    print("🔐 Checking ngrok authentication...")
    
    try:
        result = subprocess.run(['ngrok', 'config', 'check'], 
                              capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ ngrok authentication is working")
            return True
        else:
            print("❌ ngrok authentication failed")
            print(f"Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error checking ngrok auth: {e}")
        return False

def setup_ngrok_auth():
    """Guide user through ngrok authentication setup"""
    print("\n🔧 Setting up ngrok authentication...")
    print("=" * 50)
    print("1. Go to: https://dashboard.ngrok.com/get-started/your-authtoken")
    print("2. Sign up or log in to your ngrok account")
    print("3. Copy your authtoken")
    print("4. Come back here and paste it")
    print("=" * 50)
    
    auth_token = input("Enter your ngrok authtoken: ").strip()
    
    if not auth_token:
        print("❌ No token provided")
        return False
    
    try:
        # Add the authtoken
        result = subprocess.run(['ngrok', 'config', 'add-authtoken', auth_token], 
                              capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ ngrok authtoken added successfully!")
            return True
        else:
            print(f"❌ Failed to add authtoken: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error adding authtoken: {e}")
        return False

def test_ngrok_after_auth():
    """Test ngrok after authentication"""
    print("\n🧪 Testing ngrok after authentication...")
    
    try:
        # Try to start ngrok briefly
        process = subprocess.Popen(['ngrok', 'http', '5000'], 
                                 stdout=subprocess.DEVNULL, 
                                 stderr=subprocess.DEVNULL)
        
        # Wait a moment
        import time
        time.sleep(3)
        
        # Check if ngrok is running
        import requests
        try:
            response = requests.get('http://localhost:4040/api/tunnels', timeout=2)
            if response.status_code == 200:
                tunnels = response.json()['tunnels']
                if tunnels:
                    print("✅ ngrok is working! Found tunnel:")
                    print(f"   URL: {tunnels[0]['public_url']}")
                    process.terminate()
                    return True
        except:
            pass
        
        process.terminate()
        print("❌ ngrok test failed")
        return False
        
    except Exception as e:
        print(f"❌ Error testing ngrok: {e}")
        return False

def main():
    print("🔧 ngrok Authentication Fixer")
    print("=" * 40)
    
    # Check current auth status
    if check_ngrok_auth():
        print("✅ ngrok is already authenticated!")
        if test_ngrok_after_auth():
            print("\n🎉 Everything is working! You can now run:")
            print("   python simple_start.py")
        return
    
    # Set up authentication
    if setup_ngrok_auth():
        print("\n🧪 Testing ngrok after authentication...")
        if test_ngrok_after_auth():
            print("\n🎉 Authentication successful! You can now run:")
            print("   python simple_start.py")
        else:
            print("\n❌ ngrok still not working after authentication")
            print("💡 Try these troubleshooting steps:")
            print("1. Restart your terminal/command prompt")
            print("2. Try running: ngrok http 5000")
            print("3. Check if your firewall is blocking ngrok")
    else:
        print("\n❌ Authentication setup failed")
        print("💡 Try these manual steps:")
        print("1. Open a new terminal")
        print("2. Run: ngrok config add-authtoken YOUR_TOKEN")
        print("3. Test with: ngrok http 5000")

if __name__ == '__main__':
    main()
