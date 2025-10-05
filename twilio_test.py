import os
import time
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

account_sid = os.environ["ACCOUNT_SID"]
auth_token = os.environ["AUTH_TOKEN"]
client = Client(account_sid, auth_token)

call = client.calls.create(
    twiml="<Response><Say>Ahoy, world.</Say></Response>",
    to="+17789279764",
    from_="+17784880874",
)

print(f"Call initiated: {call.sid}")
print("Waiting for call to complete...")

# Wait for the call to complete by checking its status
while True:
    call_status = client.calls(call.sid).fetch()
    print(f"Call status: {call_status.status}")

    if call_status.status in ["completed", "busy", "no-answer", "failed", "canceled"]:
        print(f"Call finished with status: {call_status.status}")
        break

    time.sleep(2)  # Check every 2 seconds

print("Call process completed!")
