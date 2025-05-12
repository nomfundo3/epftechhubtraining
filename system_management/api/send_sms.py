import os
from django.conf import settings
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

client = Client(settings.ACCOUNT_SID, settings.AUTH_TOKEN)

def send_otp(first_name, last_name, user_code, phone_number):
    deep_ocr = "🔍 Deep OCR 🔍"
    greeting = f" Hi {first_name} {last_name}! "
    otp_text = f"Your OTP: {user_code} "

    fancy_message = f"{deep_ocr}\n\n{greeting}\n\n{otp_text}"

    message = client.messages.create(
        body=fancy_message,
        from_='+27600918430',
        to=f'{phone_number}'
    )
