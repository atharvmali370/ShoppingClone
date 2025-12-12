from userapp.models import User , UserProfile
from django.dispatch import receiver
from django.db.models.signals import (
    post_save,
    pre_save,
)


@receiver(post_save, sender=User)
def create_profile(sender, instance, created , *args ,**kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance , *args ,**kwargs):
    instance.userprofile.save()
