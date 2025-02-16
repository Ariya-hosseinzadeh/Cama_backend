from django.contrib import admin

from complaint_ticket.models import *
from complaint_ticket.views import ComplaintsList

# Register your models here.
admin.site.register(Complaint)
