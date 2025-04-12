from django.urls import path, include


from Rating import admin
from .  import views
from .views import AdminDashboardView, EmployeeDashboardView, VerifyEmailView, ProvinceViewSet
from rest_framework.routers import DefaultRouter
from .views import CityViewSet
router = DefaultRouter()
router.register(r'cities', CityViewSet, basename='city')
router.register(r'province', ProvinceViewSet, basename='province')

urlpatterns = [
path('isadmin/', views.UserViewSet.as_view(), name='admin'),
path('employee/', views.IsEmployeeUser, name='employee'),
path('sign-up/', views.UserSignup.as_view(), name='signup'),
path('login/', views.UserLoginView.as_view(), name='login'),
path('verify-email/<str:token>/', VerifyEmailView.as_view(), name='verify-email'),
path('admin-dashboard/', AdminDashboardView.as_view(), name='admin-dashboard'),
    path('employee-dashboard/', EmployeeDashboardView.as_view(), name='employee-dashboard'),
    path('send-again/',views.SendAgainVerifiedView.as_view(), name='send-again'),
    path('recovery-password/', views.RecoverypasswordView.as_view(), name='recovery-password'),
    path('verify-password/<str:token>/', views.VerifyRecoveryPasswordView.as_view(), name='verify-password'),

    path('user-current/', views.UserCurrentView.as_view(), name='user_current'),
    path('refresh-token/',views.CustomTokenRefreshView.as_view(), name='token_refresh' ),
    path('coustom-log-out/', views.UserLogoutView.as_view(), name='custom-logout'),
    path('profile-information/',views.UserProfileView.as_view(), name='profile-information'),
    path('images-profile/',views.SelectImageProfileView.as_view(), name='images-profile'),
    path('',include(router.urls)),
]