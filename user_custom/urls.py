from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

from Rating import admin
from .  import views
from .views import AdminDashboardView, EmployeeDashboardView, VerifyEmailView

urlpatterns = [
path('isadmin/', views.UserViewSet.as_view(), name='admin'),
path('employee/', views.IsEmployeeUser, name='employee'),
path('signup/', views.UserSignup.as_view(), name='signup'),
path('login/', views.UserLoginView.as_view(), name='login'),
path('verify-email/<str:token>/', VerifyEmailView.as_view(), name='verify-email'),
path('admin-dashboard/', AdminDashboardView.as_view(), name='admin-dashboard'),
    path('employee-dashboard/', EmployeeDashboardView.as_view(), name='employee-dashboard'),
    path('send-again/',views.SendAgainVerifiedView.as_view(), name='send-again'),
    path('recovery-password/', views.RecoverypasswordView.as_view(), name='recovery-password'),
    path('verify-password/<str:token>/', views.VerifyRecoveryPasswordView.as_view(), name='verify-password'),
path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]