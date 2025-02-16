from django.db.models.signals import pre_save
from django.dispatch import receiver

from Tags.models import Tag
from classroom.models import Course


@receiver(pre_save, sender=Course)
def auto_assign_tags(sender, instance, **kwargs):
    if instance.category:
        tags = Tag.objects.filter(categories__in=instance.category.get_ancestors(include_self=True))
        instance.tags.set(tags)
