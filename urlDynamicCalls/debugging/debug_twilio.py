#!/usr/bin/env python3
"""
Debug Twilio XML issues
This script helps identify problems with TwiML responses
"""

import requests
import json
import xml.etree.ElementTree as ET
from datetime import datetime

def validate_twiml(xml_content):
    """Validate TwiML XML format"""
    print("🔍 Validating TwiML format...")
    
    try:
        # Parse the XML
        root = ET.fromstring(xml_content)
        
        # Check if it's a valid TwiML Response
        if root.tag != 'Response':
            print("❌ Root element must be 'Response'")
            return False
        
        print("✅ Valid TwiML format")
        
        # Check for common TwiML elements
        valid_elements = ['Say', 'Play', 'Record', 'Gather', 'Redirect', 'Hangup', 'Pause']
        for elem in root:
            if elem.tag not in valid_elements:
                print(f"⚠️  Unknown element: {elem.tag}")
        
        return True
        
    except ET.ParseError as e:
        print(f"❌ XML parsing error: {e}")
        return False
    except Exception as e:
        print(f"❌ Validation error: {e}")
        return False

def test_server_endpoint(ngrok_url, script_name):
    """Test the server endpoint directly"""
    print(f"\n🌐 Testing server endpoint: {ngrok_url}/{script_name}")
    
    try:
        response = requests.get(f"{ngrok_url}/{script_name}", timeout=10)
        
        print(f"Status Code: {response.status_code}")
        print(f"Content-Type: {response.headers.get('content-type', 'Not set')}")
        print(f"Response Length: {len(response.text)} characters")
        
        if response.status_code == 200:
            print("✅ Server responded successfully")
            print(f"Content Preview: {response.text[:200]}...")
            
            # Validate the response
            if validate_twiml(response.text):
                print("✅ TwiML is valid")
                return True
            else:
                print("❌ TwiML validation failed")
                return False
        else:
            print(f"❌ Server error: {response.status_code}")
            print(f"Error content: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_update_process(ngrok_url, script_name, test_content):
    """Test the update process"""
    print(f"\n🔄 Testing update process for {script_name}...")
    
    try:
        # Get current content
        print("📥 Getting current content...")
        get_response = requests.get(f"{ngrok_url}/get/{script_name}", timeout=5)
        if get_response.status_code == 200:
            print("✅ Retrieved current content")
        else:
            print(f"❌ Failed to get current content: {get_response.status_code}")
        
        # Update content
        print("📤 Updating content...")
        update_data = {
            'content': test_content,
            'description': f'Debug test at {datetime.now()}'
        }
        
        update_response = requests.post(f"{ngrok_url}/update/{script_name}", 
                                      json=update_data, timeout=5)
        
        if update_response.status_code == 200:
            print("✅ Update successful")
        else:
            print(f"❌ Update failed: {update_response.status_code}")
            print(f"Error: {update_response.text}")
            return False
        
        # Test the updated endpoint
        print("🧪 Testing updated endpoint...")
        return test_server_endpoint(ngrok_url, script_name)
        
    except Exception as e:
        print(f"❌ Update process error: {e}")
        return False

def main():
    print("🔧 Twilio XML Debugger")
    print("=" * 40)
    
    # Get ngrok URL from user
    ngrok_url = input("Enter your ngrok URL (e.g., https://abc123.ngrok.io): ").strip()
    if not ngrok_url:
        print("❌ No URL provided")
        return
    
    # Remove trailing slash if present
    ngrok_url = ngrok_url.rstrip('/')
    
    print(f"\n🎯 Testing with URL: {ngrok_url}")
    
    # Test basic server connectivity
    print("\n1️⃣ Testing basic server connectivity...")
    if not test_server_endpoint(ngrok_url, 'script1'):
        print("❌ Basic server test failed")
        return
    
    # Test the problematic update
    print("\n2️⃣ Testing the problematic update...")
    test_xml = '<?xml version="1.0" encoding="UTF-8"?><Response><Say>Dynamic update!</Say></Response>'
    
    if test_update_process(ngrok_url, 'script1', test_xml):
        print("✅ Update test passed!")
    else:
        print("❌ Update test failed")
    
    # Test with a simpler XML
    print("\n3️⃣ Testing with simpler XML...")
    simple_xml = '<?xml version="1.0" encoding="UTF-8"?><Response><Say>Hello World!</Say></Response>'
    
    if test_update_process(ngrok_url, 'script1', simple_xml):
        print("✅ Simple XML test passed!")
    else:
        print("❌ Simple XML test failed")
    
    print("\n📋 Debug Summary:")
    print("=" * 40)
    print("If all tests pass but Twilio still fails:")
    print("1. Check Twilio webhook logs in your dashboard")
    print("2. Verify the ngrok URL is accessible from Twilio's servers")
    print("3. Try a different XML format")
    print("4. Check if there are any special characters in the XML")

if __name__ == '__main__':
    main()
