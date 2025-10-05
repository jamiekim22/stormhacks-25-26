import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

account_sid = os.getenv('Twilio_Account')
auth_token = os.getenv('Twilio_Token')
client = Client(account_sid, auth_token)

call = client.calls.create(
    url = 'https://judgementally-unlettered-carrie.ngrok-free.dev/script1',
    to="+16047832553", # this is my number, will automate to replace it later
    from_="+16043052858", # number which places the call, when business use multiple
)

print(call)