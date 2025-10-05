#!/usr/bin/env python3
"""
Script to dynamically update XML content for Twilio
Usage: refer to README_ngrok.md under usage and Test Dynamic Updates
"""

import requests
import argparse

SERVER_URL = "https://judgementally-unlettered-carrie.ngrok-free.dev"

def update_script(script_name, content):
    """Update a script with new content"""
    url = f"{SERVER_URL}/update/{script_name}"
    data = {"content": content}
    
    try:
        print(f"Updating {script_name}...")
        response = requests.post(url, json=data, timeout=10)
        
        if response.status_code == 200:
            print(f"Successfully updated {script_name}")
            return True
        else:
            print(f"Error updating {script_name}: HTTP {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to server. Make sure the Flask server is running.")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Update Twilio XML scripts')
    parser.add_argument('script', help='Script name (script1, script2)')
    parser.add_argument('content', help='XML content')
    
    args = parser.parse_args()
    
    success = update_script(args.script, args.content)
    
    if success:
        print("Update completed successfully!")
    else:
        print("Update failed.")

if __name__ == "__main__":
    main()