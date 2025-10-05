from flask import Flask, request, Response
from datetime import datetime
import os

app = Flask(__name__)

# Create recordings directory if it doesn't exist
if not os.path.exists('recordings'):
    os.makedirs('recordings')

# Store the public URL for redirects
PUBLIC_URL = None

def set_public_url(url):
    """Set the public URL for redirects"""
    global PUBLIC_URL
    PUBLIC_URL = url

# In-memory storage for dynamic XML content
xml_content = {
    'script1': '''<?xml version="1.0" encoding="UTF-8"?>
<Response>
<Say voice="woman">Hello! Please speak after the beep.</Say>
<Record maxLength="10" action="/record_handler" method="POST" recordingStatusCallback="/recording_status" />
<Redirect method="POST">http://localhost:5000/script2</Redirect>
</Response>''',
    
    'script2': '''<?xml version="1.0" encoding="UTF-8"?>
<Response>
<Say voice="man">We are in script 2</Say>
<Redirect method="POST">http://localhost:5000/script1</Redirect>
</Response>'''
}

@app.route('/script1', methods=['GET', 'POST'])
def script1():
    """Serve script1.xml with dynamic content"""
    return Response(xml_content['script1'], mimetype='application/xml')

@app.route('/script2', methods=['GET', 'POST'])
def script2():
    """Serve script2.xml with dynamic content"""
    return Response(xml_content['script2'], mimetype='application/xml')

@app.route('/record_handler', methods=['POST'])
def record_handler():
    """Handle recording completion"""
    recording_url = request.form.get('RecordingUrl')
    call_sid = request.form.get('CallSid')
    duration = request.form.get('RecordingDuration')
    
    print(f"[{datetime.now()}] Recording completed:")
    print(f"  Call SID: {call_sid}")
    print(f"  Duration: {duration} seconds")
    print(f"  Recording URL: {recording_url}")
    
    # Download the recording in background
    if recording_url:
        try:
            download_recording(recording_url, call_sid)
        except Exception as e:
            print(f"Error downloading recording: {e}")
    
    # Continue with next TwiML
    redirect_url = PUBLIC_URL or "http://localhost:5000"
    
    return Response(f'''<?xml version="1.0" encoding="UTF-8"?>
<Response>
<Say voice="woman">Recording saved. Continuing...</Say>
<Redirect method="POST">{redirect_url}/script2</Redirect>
</Response>''', mimetype='application/xml')

@app.route('/recording_status', methods=['POST'])
def recording_status():
    """Handle recording status updates"""
    status = request.form.get('RecordingStatus')
    call_sid = request.form.get('CallSid')
    
    print(f"[{datetime.now()}] Recording status: {status} for call {call_sid}")
    
    return '', 200

def download_recording(recording_url, call_sid):
    """Download recording from Twilio and save as MP3"""
    try:
        import requests
        from dotenv import load_dotenv
        
        # Load environment variables for Twilio credentials
        load_dotenv()
        account_sid = os.getenv('Twilio_Account')
        auth_token = os.getenv('Twilio_Token')
        
        if not account_sid or not auth_token:
            print("Warning: Twilio credentials not found. Recording URL saved but not downloaded.")
            print(f"Recording URL: {recording_url}")
            return None
        
        # Download the recording with Twilio authentication
        response = requests.get(recording_url, auth=(account_sid, auth_token))
        if response.status_code == 200:
            # Save as MP3 file
            filename = f"recordings/recording_{call_sid}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
            with open(filename, 'wb') as f:
                f.write(response.content)
            
            print(f"Recording saved as: {filename}")
            return filename
        else:
            print(f"Failed to download recording: HTTP {response.status_code}")
            return None
    except Exception as e:
        print(f"Error downloading recording: {e}")
        return None

@app.route('/update/<script_name>', methods=['POST'])
def update_script(script_name):
    """Update XML content dynamically"""
    if script_name not in xml_content:
        return {'error': 'Script not found'}, 404
    
    data = request.get_json()
    if 'content' not in data:
        return {'error': 'Content field required'}, 400
    
    xml_content[script_name] = data['content']
    print(f"[{datetime.now()}] Updated {script_name}")
    
    return {'status': 'success', 'message': f'{script_name} updated successfully'}

@app.route('/recordings', methods=['GET'])
def list_recordings():
    """List all recordings"""
    recordings = []
    if os.path.exists('recordings'):
        for filename in os.listdir('recordings'):
            if filename.endswith('.mp3'):
                filepath = os.path.join('recordings', filename)
                size = os.path.getsize(filepath)
                recordings.append({
                    'filename': filename,
                    'size': size,
                    'path': filepath
                })
    
    return {'recordings': recordings}

if __name__ == '__main__':
    print("Starting Twilio XML Server with Recording...")
    print("Server will be available at: http://localhost:5000")
    print("Recordings will be saved in: ./recordings/")
    app.run(host='0.0.0.0', port=5000, debug=True)