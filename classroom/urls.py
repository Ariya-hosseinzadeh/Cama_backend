from tkinter.font import names

from django.urls import path
from .  import views
urlpatterns = [
    path('create-request-course/', views.CreateRequestCourse.as_view(), name='rquest-course'),
    path('hall-waiting/',views.HallWaiting.as_view(), name='add-to-hall-waiting'),
    path('detail-request/<int:pk>',views.DetailRequset.as_view(), name='deatal-request'),
    path('invent-teacher/',views.InventationTecher.as_view(),name='inventaion-teacher'),
    path('proposers-request/<int:id>/', views.CreateProposalCourse.as_view(), name='proposers-request'),
    path('my-suggest/<int:id>',views.MySuggest.as_view(), name='my-suggest'),
    # #path('detail-course/<int:pk>/', views.DetailCourse.as_view(), name='detail-course'),
    # # path('list-course-request/', views.ListCourseRequest.as_view(), name='list-my-class'),

]