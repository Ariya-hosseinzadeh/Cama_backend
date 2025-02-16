from django.contrib import admin


from classroom.models import *

# Register your models here.

admin.site.register(Course)

admin.site.register(CourseRequest)

admin.site.register(ListCourseRequest)
admin.site.register(WaitingHall)
admin.site.register(CourseInvitation)
admin.site.register(AttentionUser)
admin.site.register(Proposal)

