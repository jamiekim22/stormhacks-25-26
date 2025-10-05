#!/usr/bin/env python3
"""
Diagnostic script to troubleshoot ngrok issues
Run this to identify what's wrong with your ngrok setup
"""

import subprocess
import requests
import os
import sys
import time

def check_ngrok_installation():
    """Check if ngrok is installed and accessible"""
    print("🔍 Checking ngrok installation...")
    
    # Try different ways to find ngrok
    ngrok_paths = [
        'ngrok',
        './ngrok.exe',
        'ngrok.exe',
        'C:\\ngrok\\ngrok.exe',
        os.path.expanduser('~/ngrok'),
    ]
    
    found_paths = []
    for path in ngrok_paths:
        try:
            result = subprocess.run([path, 'version'], check=True, capture_output=True, text=True, timeout=5)
            print(f"✅ Found ngrok at: {path}")
            print(f"   Version: {result.stdout.strip()}")
            found_paths.append(path)
        except (FileNotFoundError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
            continue
    
    if not found_paths:
        print("❌ ngrok not found in any expected location")
        print("\n💡 To fix this:")
        print("1. Download ngrok from: https://ngrok.com/download")
        print("2. Extract ngrok.exe to this project folder")
        print("3. Or add ngrok to your system PATH")
        return None
    
    return found_paths[0]  # Return the first working path

def check_ngrok_auth():
    """Check if ngrok is authenticated"""
    print("\n🔐 Checking ngrok authentication...")
    
    try:
        result = subprocess.run(['ngrok', 'config', 'check'], check=True, capture_output=True, text=True, timeout=5)
        if 'valid' in result.stdout.lower():
            print("✅ ngrok is properly authenticated")
            return True
        else:
            print("❌ ngrok authentication issue")
            print("💡 To fix: ngrok config add-authtoken YOUR_TOKEN")
            return False
    except Exception as e:
        print(f"❌ Error checking ngrok auth: {e}")
        return False

def test_ngrok_startup():
    """Test if ngrok can start properly"""
    print("\n🚀 Testing ngrok startup...")
    
    try:
        # Start ngrok in test mode
        process = subprocess.Popen(['ngrok', 'http', '5000', '--log=stdout'], 
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE,
                                 text=True)
        
        print("⏳ Waiting for ngrok to start...")
        
        # Wait and check for URL
        for i in range(10):
            time.sleep(1)
            try:
                response = requests.get('http://localhost:4040/api/tunnels', timeout=1)
                if response.status_code == 200:
                    tunnels = response.json()['tunnels']
                    if tunnels:
                        tunnel = tunnels[0]
                        print(f"✅ ngrok started successfully!")
                        print(f"   URL: {tunnel['public_url']}")
                        print(f"   Protocol: {tunnel['proto']}")
                        process.terminate()
                        return True
            except:
                pass
            print(f"   Attempt {i+1}/10: Still waiting...")
        
        print("❌ ngrok failed to start properly")
        process.terminate()
        return False
        
    except Exception as e:
        print(f"❌ Error testing ngrok startup: {e}")
        return False

def check_port_availability():
    """Check if port 5000 is available"""
    print("\n🔌 Checking port 5000 availability...")
    
    try:
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', 5000))
        sock.close()
        
        if result == 0:
            print("❌ Port 5000 is already in use")
            print("💡 To fix: Stop other services using port 5000")
            return False
        else:
            print("✅ Port 5000 is available")
            return True
    except Exception as e:
        print(f"❌ Error checking port: {e}")
        return False

def check_network_connectivity():
    """Check basic network connectivity"""
    print("\n🌐 Checking network connectivity...")
    
    try:
        response = requests.get('https://api.ngrok.com', timeout=5)
        if response.status_code == 200:
            print("✅ Network connectivity is good")
            return True
        else:
            print(f"❌ Network issue: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Network connectivity issue: {e}")
        return False

def main():
    print("🔧 ngrok Diagnostic Tool")
    print("=" * 40)
    
    # Run all checks
    ngrok_path = check_ngrok_installation()
    if not ngrok_path:
        return
    
    auth_ok = check_ngrok_auth()
    port_ok = check_port_availability()
    network_ok = check_network_connectivity()
    
    if auth_ok and port_ok and network_ok:
        print("\n🎉 All checks passed! ngrok should work.")
        print("💡 Try running: python simple_start.py")
    else:
        print("\n❌ Some issues found. Please fix them before proceeding.")
    
    print("\n📋 Summary:")
    print(f"   ngrok found: {'✅' if ngrok_path else '❌'}")
    print(f"   Authentication: {'✅' if auth_ok else '❌'}")
    print(f"   Port 5000 free: {'✅' if port_ok else '❌'}")
    print(f"   Network OK: {'✅' if network_ok else '❌'}")

if __name__ == '__main__':
    main()
