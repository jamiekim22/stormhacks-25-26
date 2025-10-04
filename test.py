import os
from twilio.rest import Client

account_sid = ''
auth_token = ''
client = Client(account_sid, auth_token)

call = client.calls.create(
    twiml = '<Response><Say>Ahoy, world.</Say></Response>',
    to="+16047832553",
    from_="+1 604 305 2858",
)



print(call)