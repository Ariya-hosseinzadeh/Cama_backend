from django.contrib import admin


from Rating.models import RatingPerson, Review, Comment

# Register your models here.

admin.site.register(RatingPerson)
admin.site.register(Review)
admin.site.register(Comment)