from django.contrib import admin

from FollowSystem.models import *
from Rating.models import Comment

# Register your models here.
admin.site.register(Follow)
admin.site.register(Post)
admin.site.register(RePost)
admin.site.register(PostMedia)
