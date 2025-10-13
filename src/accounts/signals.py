from django.db.models.signals import post_save
from django_dispatch import receiver
from .models import *

@receiver(post_save,sender=User)
def create_profile(sender,instance,create,**kwargs):
    if created:
        Profile.objects.create(user=instance)
        instance.profile.save()
        