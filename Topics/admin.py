from django.contrib import admin

from Topics.models import Topic,ResponseTopic,Vote

# Register your models here.
admin.site.register(Topic)
admin.site.register(ResponseTopic)
admin.site.register(Vote)