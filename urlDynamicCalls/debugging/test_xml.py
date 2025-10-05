#!/usr/bin/env python3
"""
Test different XML formats to find what works with Twilio
"""

import requests
import json

def test_xml_formats(ngrok_url):
    """Test various XML formats to see what works"""
    
    test_cases = [
        {
            'name': 'Basic Say',
            'xml': '<?xml version="1.0" encoding="UTF-8"?><Response><Say>Hello World!</Say></Response>'
        },
        {
            'name': 'Say with voice',
            'xml': '<?xml version="1.0" encoding="UTF-8"?><Response><Say voice="woman">Hello World!</Say></Response>'
        },
        {
            'name': 'Say with pause',
            'xml': '<?xml version="1.0" encoding="UTF-8"?><Response><Say>Hello World!</Say><Pause length="1"/></Response>'
        },
        {
            'name': 'Simple redirect',
            'xml': '<?xml version="1.0" encoding="UTF-8"?><Response><Redirect>http://example.com</Redirect></Response>'
        },
        {
            'name': 'Hangup',
            'xml': '<?xml version="1.0" encoding="UTF-8"?><Response><Say>Goodbye!</Say><Hangup/></Response>'
        }
    ]
    
    print("🧪 Testing different XML formats...")
    print("=" * 50)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. Testing: {test_case['name']}")
        print(f"   XML: {test_case['xml']}")
        
        try:
            # Update script1 with test XML
            response = requests.post(f"{ngrok_url}/update/script1", 
                                   json={'content': test_case['xml']}, timeout=5)
            
            if response.status_code == 200:
                print("   ✅ Update successful")
                
                # Test the endpoint
                test_response = requests.get(f"{ngrok_url}/script1", timeout=5)
                if test_response.status_code == 200:
                    print("   ✅ Endpoint accessible")
                    print(f"   📄 Response: {test_response.text}")
                else:
                    print(f"   ❌ Endpoint failed: {test_response.status_code}")
            else:
                print(f"   ❌ Update failed: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        print("   " + "-" * 40)

def main():
    print("🧪 Twilio XML Format Tester")
    print("=" * 40)
    
    ngrok_url = input("Enter your ngrok URL: ").strip()
    if not ngrok_url:
        print("❌ No URL provided")
        return
    
    ngrok_url = ngrok_url.rstrip('/')
    
    test_xml_formats(ngrok_url)
    
    print("\n💡 Tips:")
    print("1. Try the 'Basic Say' format first")
    print("2. If that works, try more complex formats")
    print("3. Check Twilio logs for specific error messages")
    print("4. Make sure your ngrok URL is accessible from the internet")

if __name__ == '__main__':
    main()
