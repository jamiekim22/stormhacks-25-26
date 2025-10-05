# Twilio Integration for Speech-to-Speech Pipeline

This integration allows you to use the speech-to-speech pipeline with Twilio voice calls, enabling real-time AI conversations over the phone.

## Setup

### 1. Install Dependencies

```bash
pip install twilio fastapi uvicorn websockets
```

### 2. Configure Twilio

1. **Get Twilio Credentials:**
   - Sign up at [Twilio Console](https://console.twilio.com/)
   - Get your Account SID and Auth Token
   - Purchase a phone number

2. **Update Configuration:**
   Edit `config_twilio.json`:
   ```json
   {
     "twilio_handler_kwargs": {
       "twilio_account_sid": "YOUR_ACCOUNT_SID",
       "twilio_auth_token": "YOUR_AUTH_TOKEN",
       "twilio_phone_number": "+1234567890",
       "twilio_port": 8000,
       "twilio_domain": "your-domain.com"
     }
   }
   ```

3. **Configure Webhooks:**
   - In Twilio Console, set your phone number's webhook URL to:
     `https://your-domain.com/voice`
   - Set HTTP method to POST

### 3. Deploy with Public Domain

The Twilio integration requires a publicly accessible domain for webhooks. You can use:

- **ngrok** (for testing):
  ```bash
  ngrok http 8000
  ```
  Use the ngrok URL as your domain.

- **Cloud providers** (for production):
  - AWS, Google Cloud, Azure
  - Heroku, Railway, Render

## Usage

### Run the Pipeline

```bash
python s2s_pipeline.py config_twilio.json
```

### Make a Call

Call your Twilio phone number. The AI will:
1. Answer the call
2. Start a media stream
3. Listen to your speech
4. Process with STT → LLM → TTS
5. Respond with generated speech

## Architecture

```
Phone Call → Twilio → Webhook → FastAPI → WebSocket → Pipeline
                ↑                                    ↓
                ← Audio Stream ← TTS ← LLM ← STT ←
```

## Components

### TwilioHandler
- **File**: `connections/twilio_handler.py`
- **Purpose**: Manages Twilio voice calls and media streams
- **Features**:
  - Webhook handling for call events
  - WebSocket for bidirectional audio streaming
  - Base64 audio encoding/decoding
  - Queue integration with pipeline

### Configuration
- **File**: `config_twilio.json`
- **Purpose**: Configure all pipeline components for Twilio
- **Components**:
  - Twilio credentials
  - STT settings (Whisper)
  - LLM settings (OpenAI API)
  - TTS settings (ElevenLabs)

## Audio Format

- **Sample Rate**: 8kHz (Twilio standard)
- **Channels**: 1 (mono)
- **Format**: PCM, base64 encoded
- **Chunk Size**: 1024 bytes

## Troubleshooting

### Common Issues

1. **Webhook not receiving calls:**
   - Check domain is publicly accessible
   - Verify webhook URL in Twilio Console
   - Check firewall/port settings

2. **Audio quality issues:**
   - Adjust VAD threshold in config
   - Check STT/TTS model settings
   - Verify audio format compatibility

3. **Connection timeouts:**
   - Increase timeout values
   - Check network stability
   - Monitor server resources

### Debug Mode

Enable debug logging:
```json
{
  "module_kwargs": {
    "log_level": "debug"
  }
}
```

## Security

- Store credentials in environment variables
- Use HTTPS for webhooks
- Implement rate limiting
- Validate webhook signatures

## Scaling

For production use:
- Use load balancers
- Implement connection pooling
- Monitor resource usage
- Set up health checks

## Example Use Cases

- **Customer Service**: AI-powered phone support
- **Appointments**: Automated scheduling calls
- **Surveys**: Voice-based data collection
- **Education**: Interactive learning calls
- **Accessibility**: Voice interfaces for users
