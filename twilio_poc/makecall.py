"""
Start a Twilio call with Media Streams using your Cloudflare Tunnel
"""

import os
import time
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()


def start_demo_call():
    """Start a call with Media Streams"""

    account_sid = os.environ["ACCOUNT_SID"]
    auth_token = os.environ["AUTH_TOKEN"]
    client = Client(account_sid, auth_token)

    # Replace with your Cloudflare Tunnel URL
    # Format: wss://your-tunnel-url.trycloudflare.com
    CLOUDFLARE_TUNNEL_URL = "wss://0a5f43b0c7fb.ngrok-free.app/media"

    print(f"Starting call with Media Streams...")
    print(f"WebSocket URL: {CLOUDFLARE_TUNNEL_URL}")

    # Create call with Media Streams
    call = client.calls.create(
        # twiml=f'''
        # <Response>
        #     <Start>
        #         <Stream url="{CLOUDFLARE_TUNNEL_URL}"/>
        #     </Start>
        #     <Say>Hello! This is a real-time audio call with Media Streams.</Say>
        #     <Pause length="3"/>
        #     <Say>You should hear your voice echoed back to you.</Say>
        #     <Pause length="5"/>
        #     <Say>Goodbye!</Say>
        # </Response>
        # ''',
        twiml="""
        <Response>
          <Connect>
            <Stream url="wss://0a5f43b0c7fb.ngrok-free.app/media" />
          </Connect>
        </Response>""",
        to="+17788888888",  # Replace with your phone number
        from_="+17784880874",  # Replace with your Twilio number
    )

    print(f"Call initiated: {call.sid}")
    print("Waiting for call to complete...")

    # Wait for call to complete
    while True:
        call_status = client.calls(call.sid).fetch()
        print(f"Call status: {call_status.status}")

        if call_status.status in [
            "completed",
            "busy",
            "no-answer",
            "failed",
            "canceled",
        ]:
            print(f"Call finished with status: {call_status.status}")
            break

        time.sleep(2)

    print("Demo completed!")


if __name__ == "__main__":
    start_demo_call()
