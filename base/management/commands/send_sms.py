from django.core.management.base import BaseCommand
from twilio.rest import Client
from django.conf import settings

class Command(BaseCommand):
    help = 'Sends an SMS using Twilio'

    def handle(self, *args, **options):
        account_sid = settings.TWILIO_ACCOUNT_SID
        auth_token = settings.TWILIO_AUTH_TOKEN
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            from_='+12566458642',
            to='+256758969973',
            body='Hello from Twilio!'  # Optional message body
        )

        self.stdout.write(self.style.SUCCESS(f'SMS sent! Message SID: {message.sid}'))
