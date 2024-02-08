from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import StaffProfile
# If create or update user is staff, update staff model
@receiver(post_save, sender=User)
def create_staff_profile(sender, instance, created, **kwargs):
    if created and instance.is_staff:
            StaffProfile.objects.create(user=instance, hire_date=instance.date_joined)

@receiver(post_save, sender=User)
def update_staff_profile(sender, instance, **kwargs):
    if instance.is_staff:
        instance.staffprofile.save()
