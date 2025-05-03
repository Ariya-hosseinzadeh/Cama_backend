from pyclbr import Class
from classroom.models import *
from django.db import models
from django.utils.text import slugify
from mptt.models import MPTTModel, TreeForeignKey
# Create your models here.
# class Category(MPTTModel):
#     name = models.CharField(max_length=255, unique=True)
#     slug = models.SlugField(max_length=255, unique=True, blank=True)
#     parent = TreeForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="subcategories")
#class MPTTMeta:
    #order_insertion_by = ["name"]
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="subcategories")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'
