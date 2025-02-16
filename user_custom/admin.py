from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from user_custom.models import CustomUser, Skills
from  user_custom.models import AdditionalInformationUser
from user_custom.models import Employee


# Register your models here.
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(AdditionalInformationUser)
admin.site.register(Employee)
admin.site.register(Skills)
