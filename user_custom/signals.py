from django.db.models.signals import post_save
from django.dispatch import receiver


from user_custom.models import CustomUser, AdditionalInformationUser


@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        AdditionalInformationUser.objects.create(user=instance)
