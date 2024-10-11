from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User, UserProfile



@receiver(post_save, sender=User)   
def post_save_create_profile(sender, instance, created, **kwargs):
    print(created)
    if created:
        UserProfile.objects.create(user=instance)
        print("User-Profile created!")
    else:
        try:
            profile = UserProfile.objects.get(user=instance)
            profile.save()
        except:
            # create the user profile if not exist.
            UserProfile.objects.create(user=instance)
            print("Profile was not exsit, but I created one!")
        print("User is updated!")


# post_save.connect(post_save_create_profile, sender=User)