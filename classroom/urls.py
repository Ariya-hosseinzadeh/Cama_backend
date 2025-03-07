from tkinter.font import names
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .  import views
urlpatterns = [
    path('request-course/', views.CreateRequestCourse.as_view(), name='rquest-course'),
    path('hall-waiting/',views.HallWaiting.as_view(), name='add-to-hall-waiting'),
    path('detail-request/<int:pk>',views.DetailRequest.as_view(), name='deatal-request'),
    path('invent-teacher/<int:id>',views.InventationTecher.as_view(),name='inventaion-teacher'),
    path('proposers-request/<int:id>/', views.CreateProposalCourseRequest.as_view(), name='proposers-request'),
    path('my-suggest/<int:id>',views.MySuggest.as_view(), name='my-suggest'),
    path('create-course/',views.CreateCourse.as_view(), name='create-course'),
    path('my-inventation-recive/', views.myInventationRecive.as_view(), name='my-inventation'),
    path('detail-my-inventation-recive/<int:id>',views.detalMyInventationRecive.as_view(), name='detail-inventation'),
    path('my-inventation-send/',views.myInventationSend.as_view(), name='my-inventation-send'),
    path('detail-my-inventation-send/<int:id>',views.detailMyInventationSend.as_view(), name='detailMyInventationSend'),
    path('response-proposers/<int:id>',views.ResponseProposalCourseRequest.as_view(), name='response-proposers'),
    path('detail-create/<int:pk>',views.detailCreateCourse.as_view(), name='detail-create'),
    # #path('detail-course/<int:pk>/', views.DetailCourse.as_view(), name='detail-course'),
    # # path('list-course-request/', views.ListCourseRequest.as_view(), name='list-my-class'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)