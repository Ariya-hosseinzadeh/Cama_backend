# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import *
# from Tags.models import *
#
# @receiver(post_save, sender=CourseRequest)
# def assign_tags_to_class(sender, instance, created, **kwargs):
#     """بعد از ایجاد یک کلاس، تگ‌ها را بر اساس دسته‌بندی‌های آن تنظیم می‌کند"""
#     if created:  # فقط هنگام ایجاد کلاس جدید اجرا شود
#         tags = set()  # مجموعه‌ای برای نگهداری تگ‌ها (بدون تکرار)
#
#         # بررسی دسته‌بندی‌های کلاس و افزودن تگ‌ها
#         category = instance.category
#         while category:
#             tags.add(category.name)  # نام دسته‌بندی را به عنوان تگ اضافه کن
#             category = category.parent  # بررسی دسته‌بندی‌های بالاتر
#
#         # تبدیل نام‌ها به اشیاء تگ و افزودن آنها به کلاس
#         tag_objects = [Tag.objects.get_or_create(name=tag)[0] for tag in tags]
#         instance.tags.set(tag_objects)  # تگ‌ها را به کلاس اختصاص بده

