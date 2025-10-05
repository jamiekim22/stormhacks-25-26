from dataclasses import dataclass
from typing import Optional


@dataclass
class TwilioHandlerArguments:
    """Arguments for Twilio handler configuration."""
    
    # Twilio credentials
    twilio_account_sid: Optional[str] = None
    twilio_auth_token: Optional[str] = None
    twilio_phone_number: Optional[str] = None
    twilio_user_number: Optional[str] = None  # Number to call automatically
    
    # Server configuration
    twilio_port: int = 8000
    twilio_domain: Optional[str] = None  # Your public domain for webhooks
    
    # Audio configuration
    twilio_sample_rate: int = 8000  # Twilio uses 8kHz
    twilio_channels: int = 1
    twilio_chunk_size: int = 1024
