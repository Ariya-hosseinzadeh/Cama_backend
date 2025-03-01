from django.db import models

# from classroom.models import Course
# from user_custom.models import CustomUser
#
#
# # Create your models here.
# class Complaint(models.Model):
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE,related_name='complainant')
#     title = models.CharField(max_length=100)
#     description = models.TextField()
#     audience = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
#     course=models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
#     date = models.DateField(auto_now=True)
#     def __str__(self):
#         return self.title
