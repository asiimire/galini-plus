from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import BroadcastMessage, User, Profile, Meep
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import MeepForm, SignUpForm, ProfilePicForm, AppointmentForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from django.core.mail import EmailMessage
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import validate_email as django_validate_email
from django.db.models import Q

# from django.views.generic import ListView, DetailView

# phq9 calc
def phq9_calculator(request):
    return render(request, 'phq9_calculator.html')

# home section
def home(request):
    if request.user.is_authenticated:
        form = MeepForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                meep = form.save(commit=False)
                meep.user = request.user
                meep.save()
                messages.success(request, "Your meep has been posted!")
                return redirect("home")
        meeps = Meep.objects.all().order_by("-created_at")
        return render(request, "home.html", {"meeps": meeps, "form": form})
    else:
        meeps = Meep.objects.all().order_by("-created_at")
        return render(request, "home.html", {"meeps": meeps})

# class HomeView(ListView):
#     model = Meep
#     template_name = 'home.html'

# profile section
def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, "profile_list.html", {"profiles": profiles})
    else:
        messages.success(request, "Please login to view this page.")
        return redirect("home")


def unfollow(request, pk):
    if request.user.is_authenticated:
        # get the profile to unfollow
        profile = Profile.objects.get(user_id=pk)
        # unfollow the user
        request.user.profile.follows.remove(profile)
        # save our profile
        request.user.profile.save()
        # return message
        messages.success(
            request, f"You have successfully unfollowed {profile.user.username}"
        )
        return redirect(request.META.get("HTTP_REFERER"))
    else:
        messages.error(request, "You must be logged in to unfollow")
        return redirect("home")


def follow(request, pk):
    if request.user.is_authenticated:
        # get the profile to follow
        profile = Profile.objects.get(user_id=pk)
        # follow the user
        request.user.profile.follows.add(profile)
        # save our profile
        request.user.profile.save()
        # return message
        messages.success(
            request, f"You have successfully followed {profile.user.username}"
        )
        return redirect(request.META.get("HTTP_REFERER"))
    else:
        messages.error(request, "You must be logged in to follow")
        return redirect("home")


def followers(request, pk):
    if request.user.is_authenticated:
        if request.user.id == pk:
            profiles = Profile.objects.get(user_id=pk)
            return render(request, "followers.html", {"profiles": profiles})
        else:
            messages.success(request, "That's not your profile page.")
            return redirect("home")
    else:
        messages.success(request, "Please login to view this page.")
        return redirect("home")


def follows(request, pk):
    if request.user.is_authenticated:
        if request.user.id == pk:
            profiles = Profile.objects.get(user_id=pk)
            return render(request, "follows.html", {"profiles": profiles})
        else:
            messages.success(request, "That's not your profile page.")
            return redirect("home")
    else:
        messages.success(request, "Please login to view this page.")
        return redirect("home")


def profile(request, pk):
    if request.user.is_authenticated:
        profile = get_object_or_404(Profile, user_id=pk)
        meeps = Meep.objects.filter(user_id=pk).order_by("-created_at")
        # post form logic
        if request.method == "POST":
            # get current user id
            current_user_profile = request.user.profile
            # get form data
            action = request.POST["follow"]
            # check if action is 'follow' or 'unfollow'
            if action == "follow":
                current_user_profile.follows.add(profile)
            elif action == "unfollow":
                current_user_profile.follows.remove(profile)
            else:
                messages.error(request, "Invalid action")
            # save the profile
            current_user_profile.save()

        return render(request, "profile.html", {"profile": profile, "meeps": meeps})
    else:
        messages.success(request, "Please login to view profiles")
        return redirect("home")


# authentication section
def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You are now logged in")
            return redirect("home")
        else:
            messages.error(request, "There was an error logging in. Please try again")
            return redirect("login")
    else:
        return render(request, "login.html", {})


def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out")
    return redirect("home")


def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]

            # Authenticate and log in the user
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "You have been registered successfully. Please update your profile.")
                return redirect("update_profile")  # Redirect to the profile update page instead of home

    return render(request, "register.html", {"form": form})


def update_profile(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        profile_user = Profile.objects.get(user__id=request.user.id)
        
        # Store the original firstname and lastname
        original_firstname = current_user.first_name
        original_lastname = current_user.last_name

        # Get forms
        user_form = SignUpForm(
            request.POST or None, request.FILES or None, instance=current_user
        )
        profile_form = ProfilePicForm(
            request.POST or None, request.FILES or None, instance=profile_user
        )

        if user_form.is_valid() or profile_form.is_valid():
            # Save the user form with partial=True to allow only the provided fields to be updated
            user_form.save(commit=False)

            # Restore the original firstname and lastname
            current_user.first_name = original_firstname
            current_user.last_name = original_lastname

            current_user.save()  # Now save the user with the original names
            profile_form.save()  # Save profile form with any updated data

            login(request, current_user)
            messages.success(request, "Your profile has been updated successfully")
            return redirect("home")

        return render(
            request,
            "update_profile.html",
            {"user_form": user_form, "profile_form": profile_form},
        )
    else:
        messages.success(request, "Please login to view this page.")
        return redirect("home")

# def update_profile(request):
#     if request.user.is_authenticated:
#         current_user = User.objects.get(id=request.user.id)
#         profile_user = Profile.objects.get(user__id=request.user.id)
        
#         # Store the original firstname and lastname
#         original_firstname = current_user.first_name
#         original_lastname = current_user.last_name

#         # Get forms
#         user_form = SignUpForm(
#             request.POST or None, request.FILES or None, instance=current_user
#         )
#         profile_form = ProfilePicForm(
#             request.POST or None, request.FILES or None, instance=profile_user
#         )

#         # Check if either form is valid
#         if user_form.is_valid():
#             # Save the user form with partial=True to allow only the provided fields to be updated
#             user_form.save(commit=False)

#             # Restore the original firstname and lastname
#             current_user.first_name = original_firstname
#             current_user.last_name = original_lastname

#             current_user.save()  # Now save the user with the original names

#             messages.success(request, "Your profile details have been updated successfully")
#             return redirect("home")

#         if profile_form.is_valid():
#             profile_form.save()  # Save profile form with any updated data

#             messages.success(request, "Your profile image has been updated successfully")
#             return redirect("home")

#         return render(
#             request,
#             "update_profile.html",
#             {"user_form": user_form, "profile_form": profile_form},
#         )
#     else:
#         messages.success(request, "Please login to view this page.")
#         return redirect("home")


# meep section
def meep_like(request, pk):
    if request.user.is_authenticated:
        meep = get_object_or_404(Meep, id=pk)
        if meep.likes.filter(id=request.user.id):
            meep.likes.remove(request.user)
        else:
            meep.likes.add(request.user)
        # print(request.META.get('HTTP_REFERER'))
        return redirect(request.META.get("HTTP_REFERER"))
    else:
        return redirect("home")


def meep_show(request, pk):
    meep = get_object_or_404(Meep, id=pk)
    if meep:
        return render(request, "meep_show.html", {"meep": meep})
    else:
        messages.error(request, ("That meep is not available"))
        return redirect("home")


def delete_meep(request, pk):
    if request.user.is_authenticated:
        meep = get_object_or_404(Meep, id=pk)
        # check to see if you own the meep
        if request.user.username == meep.user.username:
            # delete the meep
            meep.delete()

            messages.success(request, ("The meep has been deleted..."))
            return redirect(request.META.get("HTTP_REFERER"))
        else:
            messages.error(request, ("That meep is not yours"))
            return redirect("home")
    else:
        messages.error(request, ("Please login in to continue"))
        return redirect("home")


def edit_meep(request, pk):
    if request.user.is_authenticated:
        # grab the meep
        meep = get_object_or_404(Meep, id=pk)
        if request.user.username == meep.user.username:
            # check to see if its user's meep
            form = MeepForm(request.POST or None, instance=meep)

            if request.method == "POST":
                if form.is_valid():
                    meep = form.save(commit=False)
                    meep.user = request.user
                    meep.save()
                    messages.success(request, ("Your meep updated successfully"))
                    return redirect("home")
            else:
                return render(request, "edit_meep.html", {"meep": meep, "form": form})
        else:
            messages.error(request, ("That meep is not yours"))
            return redirect("home")
    else:
        messages.error(request, ("Please login in to continue"))
        return redirect("home")

def search(request):
    if request.method == "POST":
        # grab the form field input
        search = request.POST["search"]
        # search the database
        searched = Meep.objects.filter(body__contains = search)
        return render(request, "search.html", {"search": search, 'searched': searched})
    else:
        return render(request, "search.html", {})
    
# users section

# def search_user(request):
#     if request.method == "POST":
#         # grab the form field input
#         search = request.POST["search"]
#         # search the database
#         searched = User.objects.filter(username__icontains = search)
#         return render(request, "search_user.html", {"search": search, 'searched': searched})
#     else:
#         return render(request, "search_user.html", {})

def search_user(request):
    if request.method == "POST":
        search = request.POST["search"]
        searched = User.objects.filter(Q(username__icontains = search) | Q(first_name__icontains = search) | Q(last_name__icontains = search))
        return render(request, "search_user.html", {"search": search, 'searched': searched})
    else:
        return render(request, "search_user.html", {})

# sms section
def broadcast_sms(request):
    try:
        # Fetch the latest message content from the database
        message_to_broadcast = BroadcastMessage.objects.latest("id").content
    except BroadcastMessage.DoesNotExist:
        return HttpResponse("No message to broadcast.", status=404)

    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    # Iterate through the list of recipients
    for recipient in settings.SMS_BROADCAST_TO_NUMBERS:
        print(recipient)
        if recipient:
            # Ensure recipient is in E.164 format
            if not recipient.startswith("+"):
                recipient = f"+{recipient}"
            try:
                # Send the SMS message
                client.messages.create(
                    to=recipient,
                    from_=settings.TWILIO_PHONE_NUMBER,
                    body=message_to_broadcast,
                )
            except TwilioRestException as e:
                # Log any errors during the message sending
                print(f"Failed to send message to {recipient}: {str(e)}")

    return HttpResponse(f"Messages sent: {message_to_broadcast}", status=200)


# video chat section
@login_required
def dashboard_chat(request):
    user = request.user
    name = (
        f"{user.first_name} {user.last_name}"
        if user.first_name and user.last_name
        else user.username
    )
    return render(request, "dashboard_chat.html", {"name": name})


@login_required
def videocall(request):
    user = request.user
    name = (
        f"{user.first_name} {user.last_name}"
        if user.first_name and user.last_name
        else user.username
    )
    return render(request, "mental/meeting.html", {"name": name})


@login_required
def join(request):
    if request.method == "POST":
        roomID = request.POST["roomID"]
        return redirect("/meeting?roomID=" + roomID)
    return render(request, "mental/join.html")


# appointment section
def validate_email(email):
    try:
        django_validate_email(email)
        return True
    except ValidationError:
        return False


def appointment(request):
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            # Extract data from the form
            yourname = form.cleaned_data.get("yourname")
            youremail = form.cleaned_data.get("youremail")
            yourcontact = form.cleaned_data.get("yourcontact")
            yourday = form.cleaned_data.get("yourday")
            yourtime = form.cleaned_data.get("yourtime")
            yourdoc = form.cleaned_data.get("yourdoc")
            yourmessage = form.cleaned_data.get("yourmessage")

            # Construct the email content
            subject = "New Appointment Request"
            message_body = (
                f"Name: {yourname}\n"
                f"Email: {youremail}\n"
                f"Contact: {yourcontact}\n"
                f"Day: {yourday}\n"
                f"Time: {yourtime}\n"
                f"Doctor: {yourdoc}\n"
                f"Message: {yourmessage}"
            )
            from_email = youremail
            reply_to_email = youremail

            # Validate the email address
            if not validate_email(from_email):
                return HttpResponse("Invalid email address", status=400)

            try:
                # Send the email
                email = EmailMessage(
                    subject,
                    message_body,
                    from_email,
                    ["galiniplus@gmail.com"],
                    headers={"Reply-To": reply_to_email},
                )
                email.send(fail_silently=False)
            except Exception as e:
                return HttpResponse(f"Error sending email: {str(e)}", status=500)

            # Redirect or show a success message
            return redirect("success")  # Redirect to a success page

    else:
        form = AppointmentForm()

    return render(request, "appointment.html", {"form": form})


def success_view(request):
    return render(
        request,
        "success.html",
        {"google_translate_api_key": settings.GOOGLE_TRANSLATE_API_KEY},
    )
