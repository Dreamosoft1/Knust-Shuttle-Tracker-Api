import requests
import os

def send_otp(name, phone_number):
    message = f"Hello Mr/Mrs.{name}, Welcome to Shuttle Hub."
    data = {
        'expiry': 5,
        'length': 6,
        'medium': 'sms',
        'message': message+' This is your verification code:\n%otp_code%\nPlease do not share this code with anyone.',
        'number': phone_number,
        'sender_id': 'ShuttleHub',
        'type': 'numeric',
    }

    headers = {
        'api-key': os.environ.get('ARK_API_KEY'),
    }

    url = 'https://sms.arkesel.com/api/otp/generate'
    response = requests.post(url, json=data, headers=headers)
    if response == 200:
        return "OTP sent successfully"
    else:
        r = response.json()
        return f"Failed to send OTP, {r['message']}"