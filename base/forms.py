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
        label='',  # No label
    )
    
    class Meta:
        model = Meep
        exclude = ('user', 'likes',)

# class SignUpForm(UserCreationForm):
#     email = forms.EmailField(
#         label='',
#         widget=forms.TextInput(
#             attrs={
#                 'placeholder': 'Email address',
#                 'class': 'form-control'
#             }),
#         help_text=None  # Remove help text
#     )
#     first_name = forms.CharField(
#         label='',
#         max_length=100,
#         widget=forms.TextInput(
#             attrs={
#                 'placeholder': 'First Name',
#                 'class': 'form-control'
#             }),
#         help_text=None  # Remove help text
#     )
#     last_name = forms.CharField(
#         label='',
#         max_length=100,
#         widget=forms.TextInput(
#             attrs={
#                 'placeholder': 'Last Name',
#                 'class': 'form-control'
#             }),
#         help_text=None  # Remove help text
#     )
    
#     class Meta:
#         model = User
#         fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

#     def __init__(self, *args, **kwargs):
#         super(SignUpForm, self).__init__(*args, **kwargs)
#         self.fields['username'].widget.attrs['placeholder'] = 'Username'
#         self.fields['username'].widget.attrs['class'] = 'form-control'
#         self.fields['username'].help_text = None  # Remove help text
        
#         self.fields['password1'].widget.attrs['placeholder'] = 'Password'
#         self.fields['password1'].widget.attrs['class'] = 'form-control'
#         self.fields['password1'].help_text = None  # Remove help text

#         self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
#         self.fields['password2'].widget.attrs['class'] = 'form-control'
#         self.fields['password2'].help_text = None  # Remove help text

class UserSignUpForm(UserCreationForm):
    email = forms.EmailField(
        label='',
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Email address',
                'class': 'form-control'  # Bootstrap class
            }
        )
    )
    first_name = forms.CharField(
        label='',
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'First Name',
                'class': 'form-control'  # Bootstrap class
            }
        )
    )
    last_name = forms.CharField(
        label='',
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Last Name',
                'class': 'form-control'  # Bootstrap class
            }
        )
    )
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(UserSignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'placeholder': 'Username',
            'class': 'form-control'  # Bootstrap class
        })
        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Password',
            'class': 'form-control'  # Bootstrap class
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Confirm Password',
            'class': 'form-control'  # Bootstrap class
        })

class TherapistSignUpForm(UserCreationForm):
    email = forms.EmailField(
        label='',
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Email address',
                'class': 'form-control'  # Bootstrap class
            }
        )
    )
    first_name = forms.CharField(
        label='',
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'First Name',
                'class': 'form-control'  # Bootstrap class
            }
        )
    )
    last_name = forms.CharField(
        label='',
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Last Name',
                'class': 'form-control'  # Bootstrap class
            }
        )
    )
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(TherapistSignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'placeholder': 'Username',
            'class': 'form-control'  # Bootstrap class
        })
        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Password',
            'class': 'form-control'  # Bootstrap class
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Confirm Password',
            'class': 'form-control'  # Bootstrap class
        })

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
        help_text=None  # Remove help text
    )

    profile_bio = forms.CharField(
        label='',
        max_length=100,
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Profile Bio',
                'class': 'form-control'
            }),
        help_text=None  # Remove help text
    )
    
    website_link = forms.CharField(
        label='',
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Website link',
                'class': 'form-control'
            }),
        help_text=None  # Remove help text
    )
    
    facebook_link = forms.CharField(
        label='',
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Facebook link',
                'class': 'form-control'
            }),
        help_text=None  # Remove help text
    )
    
    instagram_link = forms.CharField(
        label='',
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Instagram link',
                'class': 'form-control'
            }),
        help_text=None  # Remove help text
    )
    
    linkedin_link = forms.CharField(
        label='',
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'LinkedIn link',
                'class': 'form-control'
            }),
        help_text=None  # Remove help text
    )

    class Meta:
        model = Profile
        fields = ('profile_image', 'specialty', 'profile_bio', 'website_link', 'facebook_link', 'instagram_link', 'linkedin_link')

class AppointmentForm(forms.Form):
    yourname = forms.CharField(
        max_length=100, 
        required=True,
        widget=forms.TextInput(
            attrs={
                'required': '',
                'name': 'yourname',
                'type': 'text',
                'class': 'form-control',
                'placeholder': 'Your Name',
            }
        ),
        help_text=None  # Remove help text
    )
    youremail = forms.EmailField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'required': '',
                'name': 'youremail',
                'type': 'email',
                'class': 'form-control',
                'placeholder': 'Your Email',
            }
        ),
        help_text=None  # Remove help text
    )
    yourcontact = forms.CharField(
        max_length=100, 
        required=True,
        widget=forms.TextInput(
            attrs={
                'required': '',
                'name': 'yourcontact',
                'type': 'text',
                'class': 'form-control',
                'placeholder': 'Your Contact',
            }
        ),
        help_text=None  # Remove help text
    )
    yourday = forms.ChoiceField(
        choices=[
            ('', 'Day'),
            ('Sunday', 'Sunday'),
            ('Monday', 'Monday'),
            ('Tuesday', 'Tuesday'),
            ('Wednesday', 'Wednesday'),
            ('Thursday', 'Thursday'),
            ('Friday', 'Friday'),
            ('Saturday', 'Saturday'),
        ],
        widget=forms.Select(
            attrs={
                'required': '',
                'name': 'yourday',
                'class': 'form-control',
            }
        ),
        help_text=None  # Remove help text
    )
    yourtime = forms.ChoiceField(
        choices=[
            ('', 'Time'),
            ('9AM', '9AM'),
            ('12PM', '12PM'),
        ],
        widget=forms.Select(
            attrs={
                'required': '',
                'name': 'yourtime',
                'class': 'form-control',
            }
        ),
        help_text=None  # Remove help text
    )
    yourdoc = forms.ChoiceField(
        choices=[
            ('', 'Doctor Name'),
            ('Mr.XYZ', 'Mr.XYZ'),
            ('Mr.ABC', 'Mr.ABC'),
        ],
        widget=forms.Select(
            attrs={
                'required': '',
                'name': 'yourdoc',
                'class': 'form-control',
            }
        ),
        help_text=None  # Remove help text
    )
    yourmessage = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'name': 'yourmessage',
                'class': 'form-control',
                'placeholder': 'Your Message',
            }
        ),
        required=False,
        help_text=None  # Remove help text
    )
