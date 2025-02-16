from gc import get_objects

from django.core.serializers import get_serializer
from django.shortcuts import render
from rest_framework import viewsets, generics, status, mixins, request
from rest_framework.authtoken.admin import User
from rest_framework.permissions import IsAuthenticated, AllowAny
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response

from . import permissions
from .models import CustomUser
from .permissions import IsAdminUser, IsEmployeeUser
from .serializer import UserSerializer, EmployeeSerializer, LoginSerializer, AgainSendVerificationSerializer, \
    RecoverypaaswordSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
import jwt
import datetime
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate


class UserSignup(APIView):
    User=CustomUser
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
    def post(self, request):
        user = UserSerializer(data=request.data)
        if user.is_valid():
            if User.objects.filter(email=user.data['email']).exists():
                return Response({'message': 'Email already registered'}, status=status.HTTP_400_BAD_REQUEST)
        if user.is_valid():
            user = User.objects.create_user(username=user.data['username'], email=user.data['email'],
                                        password=user.data['password'],
                                        NationalCode=user.data['NationalCode'])

            payload = {
                'user_id': user.id,
                'exp': datetime.datetime.now(datetime. UTC) + datetime.timedelta(minutes=30),
                'iat': datetime.datetime.now(datetime. UTC),
            }
            token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
            verification_link=request.build_absolute_uri(reverse('verify-email',args=[token]))
            send_mail(
                'تایید ایمیل حساب شما  '
                , f'برای تأیید ایمیل خود روی لینک زیر کلیک کنید:\n\n{verification_link}',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            return Response({'message':'ایمیل تایید ارسال شد . لطفا ایمیل خود را چک کنید'}, status=status.HTTP_201_CREATED)
        return Response(user.errors,status=status.HTTP_400_BAD_REQUEST)
class VerifyEmailView(APIView):
    permission_classes = (AllowAny,)
    def get(self,request,token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:

                user.is_verified = True
                user.is_active = True
                user.save()
                return Response({'message': 'ایمیل با موفقیت تأیید شد! اکنون می‌توانید وارد شوید.',}, status=status.HTTP_200_OK,)
            return Response({'message': 'ایمیل قبلاً تأیید شده است.'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.ExpiredSignatureError:
            return Response({'error': 'لینک تأیید منقضی شده است.'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.DecodeError:
            return Response({'error': 'لینک تأیید نامعتبر است.'}, status=status.HTTP_400_BAD_REQUEST)

class SendAgainVerifiedView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = AgainSendVerificationSerializer
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.data['email']
            NationalCode = serializer.data['NationalCode']
            user= User.objects.get(NationalCode=NationalCode)
            payload = {
                'user_id': user.id,
                'exp': datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=30),
                'iat': datetime.datetime.now(datetime.UTC),
            }
            token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
            verification_link = request.build_absolute_uri(reverse('verify-email', args=[token]))
            send_mail(
                'تایید ایمیل حساب شما  '
                , f'برای تأیید ایمیل خود روی لینک زیر کلیک کنید:\n\n{verification_link}',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            return Response({'message': 'ایمیل تایید ارسال شد . لطفا ایمیل خود را چک کنید'},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)




class UserLoginView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        print(email, password)
        user = CustomUser.objects.get(email=email)
        print(user)
        if user is None or not user.check_password(password):
            return Response({"error": "ایمیل یا رمز عبور اشتباه است."}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.is_verified:
            return Response({"error": "لطفاً ابتدا ایمیل خود را تأیید کنید."}, status=status.HTTP_403_FORBIDDEN)

        # تولید توکن JWT
        refresh = RefreshToken.for_user(user)
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }, status=status.HTTP_200_OK)

class RecoverypasswordView(APIView):
    permission_classes = (AllowAny,)
    serializer_class=AgainSendVerificationSerializer
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.data['email']
            NationalCode = serializer.data['NationalCode']
            user= User.objects.get(NationalCode=NationalCode)
            payload = {
                'user_id': user.id,
                'exp': datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=30),
                'iat': datetime.datetime.now(datetime.UTC),
            }
            token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
            verification_link = request.build_absolute_uri(reverse('verify-password', args=[token]))
            send_mail(
                'تایید بازیابی رمز عبور حساب شما  '
                , f'برای تأیید بازیابی رمز عبور بر روی لینک زیر کلیک کنید کلیک کنید:\n\n{verification_link}',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            return Response({'message': 'ایمیل بازیابی ارسال شد . لطفا ایمیل خود را چک کنید'})
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
class VerifyRecoveryPasswordView(APIView):
    permission_classes = (AllowAny,)
    serializer_class=RecoverypaaswordSerializer
    def put(self,request,token):
        serializer = self.serializer_class(data=request.data)
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
            if serializer.is_valid():
                if(serializer.data['NationalCode'] == user.NationalCode):
                    if user.is_active:
                        serializer = self.serializer_class(user,data=request.data)
                        if serializer.is_valid():
                            serializer.save()
                            return Response({'message':'رمز عبور با موفقیت تغییر کرد '},status=status.HTTP_200_OK)
                    return Response({'message':'حساب شما غیر فعال است لطفا با پشتیبانی تماس بگیرید'},status=status.HTTP_401_UNAUTHORIZED)
                return Response({'message':'حساب مورد نظر پیدا نشد لطفا اطلاعات را درست وارد کنید'},status=status.HTTP_403_FORBIDDEN)
        except jwt.ExpiredSignatureError:
            return Response({'error': 'لینک تأیید منقضی شده است.'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.DecodeError:
            return Response({'error': 'لینک تأیید نامعتبر است.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class UserViewSet(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)

class UserEmployee(generics.CreateAPIView):
    serializer_class = EmployeeSerializer
    permission_classes = (IsAuthenticated, IsEmployeeUser)
    def get(self, request):
        return Response({"message": "Welcome to Employee Dashboard"})
class AdminDashboardView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        return Response({"message": "Welcome to Admin Dashboard"})

class EmployeeDashboardView(APIView):
    permission_classes = [IsEmployeeUser]

    def get(self, request):
        return Response({"message": "Welcome to Employee Dashboard"})

