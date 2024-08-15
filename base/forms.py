from django import forms
from .models import Meep, Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class MeepForm(forms.ModelForm):
    body = forms.CharField(
        required=True,
        widget=forms.widgets.Textarea(
            attrs={
                'placeholder': 'Write your blog...',
                'class': 'form-control'
            }),
            label='',
        )
    class Meta:
        model = Meep
        exclude = ('user', 'likes', )


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        label='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Email address',
                'class': 'form-control'
            }),
        )
    first_name = forms.CharField(
        label='',
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'First Name',
                'class': 'form-control'
            }),
        )
    last_name = forms.CharField(
        label='',
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Last Name',
                'class': 'form-control'
            }),
        )
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['username'].widget.attrs['class'] = 'form-control'
        
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].widget.attrs['class'] = 'form-control'

        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].widget.attrs['class'] = 'form-control'

class ProfilePicForm(forms.ModelForm):
    profile_image = forms.ImageField(label="Profile Picture")

    specialty = forms.CharField(
        label='',
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Specialty',
                'class': 'form-control'
            }),
        )

    profile_bio = forms.CharField(
        label='',
        max_length=100,
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Profile Bio',
                'class': 'form-control'
            }),
        )
    website_link = forms.CharField(
        label='',
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'website link',
                'class': 'form-control'
            }),
        )
    facebook_link = forms.CharField(
        label='',
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'facebook link',
                'class': 'form-control'
            }),
        )
    instagram_link = forms.CharField(
        label='',
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'instagram link',
                'class': 'form-control'
            }),
        )
    linkedin_link = forms.CharField(
        label='',
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'linkedin link',
                'class': 'form-control'
            }),
        )
    

    class Meta:
        model = Profile
        fields = ('profile_image', 'specialty', 'profile_bio', 'website_link', 'facebook_link' ,'instagram_link','linkedin_link', )

# appointment form
class AppointmentForm(forms.Form):
    yourname = forms.CharField(max_length=100, required=True)
    youremail = forms.EmailField(required=True)
    yourcontact = forms.CharField(max_length=100, required=True)
    yourday = forms.ChoiceField(choices=[
        ('', 'Day'),
        ('Sunday', 'Sunday'),
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
    ])
    yourtime = forms.ChoiceField(choices=[
        ('', 'Time'),
        ('9AM', '9AM'),
        ('12PM', '12PM'),
    ])
    yourdoc = forms.ChoiceField(choices=[
        ('', 'Doctor Name'),
        ('Mr.XYZ', 'Mr.XYZ'),
        ('Mr.ABC', 'Mr.ABC'),
    ])
    yourmessage = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}), required=False)

    def __init__(self, *args, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)
        self.fields['yourname'].widget.attrs.update({
            'required': '',
            'name': 'yourname',
            'type': 'text',
            'class': 'form-control',
            'placeholder': 'Your Name',
        })
        self.fields['youremail'].widget.attrs.update({
            'required': '',
            'name': 'youremail',
            'type': 'email',
            'class': 'form-control',
            'placeholder': 'Your Email',
        })
        self.fields['yourcontact'].widget.attrs.update({
            'required': '',
            'name': 'yourcontact',
            'type': 'text',
            'class': 'form-control',
            'placeholder': 'Your Contact',
        })
        self.fields['yourday'].widget.attrs.update({
            'required': '',
            'name': 'yourday',
            'class': 'form-control',
        })
        self.fields['yourtime'].widget.attrs.update({
            'required': '',
            'name': 'yourtime',
            'class': 'form-control',
        })
        self.fields['yourdoc'].widget.attrs.update({
            'required': '',
            'name': 'yourdoc',
            'class': 'form-control',
        })
        self.fields['yourmessage'].widget.attrs.update({
            'name': 'yourmessage',
            'class': 'form-control',
            'placeholder': 'Your Message',
        })