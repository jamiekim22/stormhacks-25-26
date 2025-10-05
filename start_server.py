#!/usr/bin/env python3
"""
Start the Twilio XML server with ngrok tunnel for public access
"""

import subprocess
import time
import requests
from server import app, xml_content

def get_ngrok_url():
    """Get the public ngrok URL"""
    try:
        response = requests.get('http://localhost:4040/api/tunnels', timeout=2)
        if response.status_code == 200:
            tunnels = response.json()['tunnels']
            for tunnel in tunnels:
                if tunnel['proto'] == 'https':
                    return tunnel['public_url']
            for tunnel in tunnels:
                if tunnel['proto'] == 'http':
                    return tunnel['public_url']
    except:
        pass
    return None

def update_server_urls(public_url):
    """Update the server XML content with public URLs"""
    # Set the public URL in the server
    from server import set_public_url
    set_public_url(public_url)
    
    xml_content['script1'] = f'''<?xml version="1.0" encoding="UTF-8"?>
<Response>
<Say voice="woman">Hello! Please speak after the beep.</Say>
<Record maxLength="10" action="{public_url}/record_handler" method="POST" recordingStatusCallback="{public_url}/recording_status" />
<Redirect method="POST">{public_url}/script2</Redirect>
</Response>'''
    
    xml_content['script2'] = f'''<?xml version="1.0" encoding="UTF-8"?>
<Response>
<Say voice="man">We are in script 2</Say>
<Redirect method="POST">{public_url}/script1</Redirect>
</Response>'''

def main():
    print("Starting Twilio XML Server with Public Access...")
    
    # Check if ngrok is available
    try:
        subprocess.run(['ngrok', 'version'], check=True, capture_output=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("ngrok not found. Please install ngrok first.")
        return
    
    # Start ngrok
    print("Starting ngrok tunnel...")
    process = subprocess.Popen(['ngrok', 'http', '5000'], 
                             stdout=subprocess.DEVNULL, 
                             stderr=subprocess.DEVNULL)
    
    # Wait for ngrok to start
    print("Waiting for ngrok to initialize...")
    for i in range(10):
        time.sleep(1)
        public_url = get_ngrok_url()
        if public_url:
            print(f"ngrok tunnel active: {public_url}")
            update_server_urls(public_url)
            break
        print(f"Attempt {i+1}/10: Still waiting...")
    
    if not public_url:
        print("Failed to start ngrok tunnel")
        return
    
    print("\nServer is ready!")
    print(f"Script 1: {public_url}/script1")
    print(f"Script 2: {public_url}/script2")
    print("\nPress Ctrl+C to stop the server")
    
    try:
        app.run(host='0.0.0.0', port=5000, debug=False)
    except KeyboardInterrupt:
        print("\nShutting down...")
        process.terminate()
        print("Server stopped")

if __name__ == '__main__':
    main()