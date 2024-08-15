from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# create meep/tweet model
class Meep(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='meeps')
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='meep_like', blank=True)

    # keep track of likes
    def number_of_likes(self):
        return self.likes.count()

    def __str__(self):
        return (
            f"{self.user} "
            f"{self.title} "
            f"{self.created_at.strftime('%b %d, %Y %I:%M %p')}: "
            f"{self.body[:50]}..."
            )

# User Profile model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(User, auto_now_add=True)
    follows = models.ManyToManyField("self",
                                related_name='followed_by',
                                symmetrical=False,
                                blank=True                                    
                                )
    profile_image = models.ImageField(upload_to='profile_images', blank=True, null=True)
    
    profile_bio = models.CharField(null=True, max_length=150, blank=True)
    website_link =models.CharField(null=True, max_length=100, blank=True)
    facebook_link =models.CharField(null=True, max_length=100, blank=True)
    instagram_link =models.CharField(null=True, max_length=100, blank=True)
    linkedin_link =models.CharField(null=True, max_length=100, blank=True)

    specialty =models.CharField(null=True, max_length=100, blank=True)

    # is_therapist = models.BooleanField(default=False) # distinguish therapist and user
    
    def __str__(self):
        return self.user.username

 
# create a new profile when new user signs up
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        
        # have the user follow themselves
        user_profile.follows.set([instance.profile.id])
        user_profile.save()
        
post_save.connect(create_profile, sender=User)

# store the messages in a database---------------------------------------------------------------- -
class BroadcastMessage(models.Model):
    content = models.TextField()

    def __str__(self):
        return self.content[:50]  # Display the first 50 characters in the admin interface

class PhoneNumber(models.Model):
    number = models.CharField(max_length=15)

    def __str__(self):
        return self.number
     