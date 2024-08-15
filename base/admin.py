from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Profile, Meep, BroadcastMessage, PhoneNumber
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from django.conf import settings


admin.site.unregister(Group)

# unregister initial user
admin.site.unregister(User)

# mix profile into user
class ProfileInline(admin.StackedInline):
    model = Profile
    
# extend User model
class UserAdmin(admin.ModelAdmin):
    model = User
    # just display the username fields on admin page
    fields = ['username']
    inlines = [ProfileInline]

# reregister user
admin.site.register(User, UserAdmin)

# register Meeps
admin.site.register(Meep)

# from old galiniapp
@admin.action(description='Send Broadcast SMS')
def send_broadcast_sms(modeladmin, request, queryset):
    if queryset.count() != 1:
        modeladmin.message_user(request, "Please select exactly one message to broadcast.", level='error')
        return

    message_to_broadcast = queryset.first().content
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    recipients = PhoneNumber.objects.all()
    for recipient in recipients:
        if recipient.number:
            if not recipient.number.startswith('+'):
                recipient.number = f'+{recipient.number}'
            try:
                client.messages.create(
                    to=recipient.number,
                    from_=settings.TWILIO_PHONE_NUMBER,
                    body=message_to_broadcast
                )
            except TwilioRestException as e:
                modeladmin.message_user(request, f"Failed to send message to {recipient.number}: {str(e)}", level='error')
                return

    modeladmin.message_user(request, "Broadcast SMS sent successfully.")

class BroadcastMessageAdmin(admin.ModelAdmin):
    list_display = ('content',)
    actions = [send_broadcast_sms]

class PhoneNumberAdmin(admin.ModelAdmin):
    list_display = ('number',)

admin.site.register(BroadcastMessage, BroadcastMessageAdmin)
admin.site.register(PhoneNumber, PhoneNumberAdmin)



