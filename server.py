from flask import Flask, request, Response
from datetime import datetime

app = Flask(__name__)

# In-memory storage for dynamic XML content
xml_content = {
    'script1': '''<?xml version="1.0" encoding="UTF-8"?>
<Response>
<Say voice="woman">We are in script 1</Say>
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

if __name__ == '__main__':
    print("Starting Twilio XML Server...")
    print("Server will be available at: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
