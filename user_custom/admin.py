from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from user_custom.models import CustomUser, Skills, Province, City, UserSkill, CareerHistory, Job
from  user_custom.models import AdditionalInformationUser
from user_custom.models import Employee


# Register your models here.
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Employee)
admin.site.register(Skills)
admin.site.register(City)
admin.site.register(Province)
admin.site.register(UserSkill)
admin.site.register(CareerHistory)
admin.site.register(Job)

class UserJobInline(admin.StackedInline):
    model = CareerHistory
    extra = 1


class UserSkillInline(admin.TabularInline):
    model = UserSkill
    extra = 1
class AdditionalInformationUserAdmin(admin.ModelAdmin):
    inlines = [UserSkillInline, UserJobInline]

admin.site.register(AdditionalInformationUser, AdditionalInformationUserAdmin)
