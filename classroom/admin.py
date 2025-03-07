from django.contrib import admin


from classroom.models import *

# Register your models here.

admin.site.register(AgreementCourseRequest)
admin.site.register(AgreementCourseCreate)
admin.site.register(CourseRequest)
admin.site.register(CourseCreate)
admin.site.register(WaitingHall)
admin.site.register(CourseInvitation)
admin.site.register(ProposalRequestCourse)
admin.site.register(ProposalCreateCourse)

