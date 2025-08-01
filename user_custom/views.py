from gc import get_objects
from http.client import responses
from http.cookiejar import Cookie

from django.core.serializers import get_serializer
from django.shortcuts import render
from pyasn1_modules.rfc3852 import id_data
from rest_framework import viewsets, generics, status, mixins, request
from rest_framework.authtoken.admin import User
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken,OutstandingToken

from . import permissions
from .models import CustomUser, AdditionalInformationUser, City, Province, UserSkill, CareerHistory, Job, Skills
from .permissions import IsAdminUser, IsEmployeeUser
from .serializer import UserSerializer, EmployeeSerializer, LoginSerializer, AgainSendVerificationSerializer, \
    RecoverypaaswordSerializer, AdditionalInformationSerializer, ImageProfileSerializer, CitySerializer, \
    ProvinceSerializer, UserSkillSerializer, CareerHistorySerializer, JobsSerializer, SkillsSerializer
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
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
                                        password=user.data['password']
                                        )

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
            #NationalCode = serializer.data['NationalCode']
            user= User.objects.get(email=email)
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
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed, NotFound, ValidationError


class UserCurrentView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get(self,request):
        user = request.user
        return Response({
            "id": user.id,
            "codeUser": user.codeUser,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name
        })


class UserLoginView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        try:
            user = CustomUser.objects.get(email=email)

            if user is None or not user.check_password(password):
                return Response({"error": "ایمیل یا رمز عبور اشتباه است."}, status=status.HTTP_401_UNAUTHORIZED)

            if not user.is_verified:
                return Response({"error": "لطفاً ابتدا ایمیل خود را تأیید کنید."}, status=status.HTTP_403_FORBIDDEN)
            if(user):
        # تولید توکن JWT
        # توکن ایجاد شده است که در کوکی ذخیره کردیم البته ما در خود کاما هم یک بخش برای ایجاد توکن دسترسی و توکن رفرش ایجاد کردیم اما چون خواستیم شخصی سازی کنیم اینجا داریم
                refresh = RefreshToken.for_user(user)

                access_token = str(refresh.access_token)
                refresh_token = str(refresh)
                response= Response({"access": str(refresh.access_token),"refresh": str(refresh),"user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name
                }}, status=status.HTTP_200_OK)
                response.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,  # جلوگیری از دسترسی جاوااسکریپت
                secure=True,  # فقط در HTTPS
                # samesite='Lax',  # محافظت در برابر CSRF
                samesite='None',#در محیط توسعه این مورد را تست کنید، اما در محیط تولید (production)، samesite='Lax' بهتر است.
                max_age=datetime.timedelta(minutes=5)  # مدت اعتبار کوکی
            )
                response.set_cookie(
                key='refresh_token',
                value=refresh_token,
                httponly=True,
                secure=True,
                # samesite='Lax',
                samesite='None',  # اجازه ارسال در درخواست‌های Cross-Site
                max_age=datetime.timedelta(days=7)  # مدت اعتبار کوکی
            )
                print(response.cookies)
                return response
        except CustomUser.DoesNotExist:
                return Response({"error": "ایمیل یا رمز عبور اشتباه است."}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
                return Response({"error": f"مشکلی رخ داده: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # response = Response({"message": "Successfully logged out"}, status=200)
            # response.delete_cookie("access_token")
            # response.delete_cookie("refresh_token")
            # return response
            # دریافت توکن از کوکی‌ها
            refresh_token = request.COOKIES.get("refresh_token")

            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()  # بی‌اعتبار کردن توکن
                is_blacklisted = BlacklistedToken.objects.filter(token=token).exists()
                print(f"Blacklist status: {is_blacklisted}")  # این را در لاگ سرور ببین
            response = Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)

            # حذف کوکی‌ها با مقدار خالی و تاریخ انقضای گذشته
            response.delete_cookie("access_token")
            response.delete_cookie("refresh_token")

            return response
        except Exception as e:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
class RecoverypasswordView(APIView):
    permission_classes = (AllowAny,)
    serializer_class=AgainSendVerificationSerializer
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.data['email']
            #NationalCode = serializer.data['NationalCode']
            user= User.objects.get(email=email)
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
                if(serializer.data['email'] == user.email):
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




#token refresh by coki
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        # گرفتن توکن رفرش از کوکی‌ها
        refresh_token = request.COOKIES.get('refresh_token')
        print('refresh_token', refresh_token,'انجام شد رفرش توکن ')
        if not refresh_token:
            return Response({"error": "Refresh token is missing from cookies."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # بررسی صحت توکن رفرش
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)

            # ارسال توکن دسترسی جدید به کاربر
            response = Response({"access": access_token}, status=status.HTTP_200_OK)

            return response
        except Exception as e:
            return Response({"error": f"Invalid refresh token: {str(e)}"}, status=status.HTTP_401_UNAUTHORIZED)

class UserProfileView(generics.GenericAPIView,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin):
    permission_classes = [IsAuthenticated]
    serializer_class = AdditionalInformationSerializer

    def get_queryset(self):
        user = self.request.user
        return AdditionalInformationUser.objects.filter(user=user)

    def get_object(self):
        return self.get_queryset().first()

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj is not None:
            return self.retrieve(request, *args, **kwargs)
        return Response({'status': 'لطفا ابتدا وارد شوید'}, status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj is not None:
            return self.update(request, *args, **kwargs)
        return Response({'status': 'لطفا ابتدا وارد شوید'}, status=status.HTTP_401_UNAUTHORIZED)



class SelectImageProfileView(APIView):
    serializer_class = ImageProfileSerializer
    permission_classes = [IsAuthenticated]
    def get_user_profile(self, request):
        try:
            user = CustomUser.objects.get(id=request.user.id)
            return user
        except CustomUser.DoesNotExist:
            return None
    def get(self, request):
        user = self.get_user_profile(request)
        if user:
            data_user = AdditionalInformationUser.objects.get(user=user)
            serializer = self.serializer_class(data_user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'status':'لطفا ابتدا به سیستم وارد شوید'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request):
        user=self.get_user_profile(request)
        if user:
            data_user=AdditionalInformationUser.objects.filter(user=user).first()
            serializer = self.serializer_class(data_user,data=request.data,)
            if serializer.is_valid():
                serializer.save()

                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'status': 'لطفا ابتدا به سیستم وارد شوید'}, status=status.HTTP_404_NOT_FOUND)


class ProvinceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer

class CityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer

    @action(detail=False)
    def by_province(self, request):
        province_id = request.query_params.get('province_id')
        if not province_id:
            return Response({"detail": "province_id is required."}, status=400)
        cities = City.objects.filter(province_id=province_id)
        return Response(CitySerializer(cities, many=True).data)

class SkillsApiView(APIView):
    permission_classes = [AllowAny]
    serializer_class = SkillsSerializer
    def get(self, request):
        skills = Skills.objects.all()
        serializer = self.serializer_class(skills, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
class UserSkillViewset(viewsets.ModelViewSet):
    queryset = UserSkill.objects.all()
    serializer_class = UserSkillSerializer
    permission_classes = [IsAuthenticated]  # فقط کاربران لاگین‌کرده
    def get_queryset(self):
        try:
            additional_info = AdditionalInformationUser.objects.get(user=self.request.user)
            return UserSkill.objects.filter(user=additional_info)
        except AdditionalInformationUser.DoesNotExist:
            raise NotFound("اطلاعات اضافی کاربر پیدا نشد.")
    def create(self, request, *args, **kwargs):
        additional_info = AdditionalInformationUser.objects.get(user=request.user)

        skill = request.data.get('skill')
        level = request.data.get('level')

        existing = UserSkill.objects.filter(user=additional_info, skill=skill).first()
        if existing:
            existing.level = level
            existing.save()
            serializer = self.get_serializer(existing)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=additional_info)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


    # def perform_create(self, serializer):
    #     additional_info = AdditionalInformationUser.objects.get(user=self.request.user)
    #     skill = serializer.validated_data['skill']
    #     level = serializer.validated_data['level']
    #
    #     obj, created = UserSkill.objects.update_or_create(
    #         user=additional_info,
    #         skill=skill,
    #         defaults={"level": level}
    #     )

        # این بخش رو اضافه کن تا response مناسبی برگرده
        self.instance = obj
    # def perform_create(self, serializer):
    #     additional_info = AdditionalInformationUser.objects.get(user=self.request.user)
    #     skill = serializer.validated_data['skill']
    #     level = serializer.validated_data['level']
    #
    #     existing = UserSkill.objects.filter(user=additional_info, skill=skill).first()
    #     if existing:
    #         existing.level = level
    #         existing.save()
    #         self.instance = existing  # ✅ این خط خیلی مهمه
    #     else:
    #         serializer.save(user=additional_info)

class CareerHistoryViewSet(viewsets.ModelViewSet):
    queryset = CareerHistory.objects.all()
    serializer_class = CareerHistorySerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        try:
            additional_info = AdditionalInformationUser.objects.get(user=self.request.user.id)
            return CareerHistory.objects.filter(user_data=additional_info)
        except AdditionalInformationUser.DoesNotExist:
            raise NotFound
    def perform_create(self, serializer):
        additional_info = AdditionalInformationUser.objects.get(user=self.request.user)
        serializer.save(user_data=additional_info)

class JobsGenericView(generics.GenericAPIView,mixins.ListModelMixin):
    queryset = Job.objects.all()
    serializer_class = JobsSerializer
    def get(self,request):
        return self.list(request)




