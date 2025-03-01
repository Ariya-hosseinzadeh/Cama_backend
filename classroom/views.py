from gc import get_objects
from operator import invert
from traceback import print_tb

from django.dispatch import receiver
from django.template.defaultfilters import title
from django.template.defaulttags import querystring
from pyexpat.errors import messages
from rest_framework.generics import ListAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import request, mixins
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView

from Dashboard.models import Notification
from user_custom.models import CustomUser
from user_custom.views import UserSignup
from .models import *
from .serializer import *
from django.urls import reverse

# Create your views here.
#در خواست ایجاد یک کلاس از طرف دانش آموز.کلاس به تالار انتظار بصورت خودکا اضافه میشود.تنها افرادی که لاگین کرده باشند حق دسترسی دارند
class CreateRequestCourse(APIView):
    # permission_classes = [IsAuthenticated]
    permission_classes = (AllowAny,)
    serializer_class = CreateRequestClassSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            course=CourseRequest.objects.get(id=serializer.data['id'])
            Addclass=WaitingHall.objects.create(ClassRequest=course)
            Addclass.save()
            return Response({'status':'کلاس شما به تالار انتظار با موفقیت اضافه شد،لطفا برای یافتن استاد/دانشجو منتظر بمانید'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#تمامی دعوت هایی که از معلمان برای کلاس هایی که تا الان داشتیم را نمایش میگذارد این نمایش بصورت یک لیست است
class myInventationRecive(generics.GenericAPIView,mixins.ListModelMixin):
    permission_classes = (AllowAny,)
    queryset=CourseInvitation.objects.filter(teacher=1)
    serializer_class = InventiationTeacherSerializer
    def get(self, request:Request):
        return self.list(request)

class myInventationSend(generics.GenericAPIView,mixins.ListModelMixin):
    permission_classes = (AllowAny,)
    queryset=CourseInvitation.objects.filter(creator=1)#change user
    serializer_class = InventiationTeacherSerializer
    def get(self, request:Request):
        return self.list(request)
#با توجه به آی دعوت به جزِئیات آن دسترسی دارد
class detalMyInventationRecive(APIView):
    permission_classes = (AllowAny,)
    serializer_class = InventiationTeacherSerializer
    def get(self, request:Request,id):
        data=CourseInvitation.objects.filter(id=id)
        serializers=self.serializer_class(data,many=True)
        return Response(serializers.data or {'status':'دعوت مد نظر یافت نشد'}, status=status.HTTP_200_OK)

    def put(self, request:Request, id):
        data=CourseInvitation.objects.get(id=id)
        serializers=self.serializer_class(data,data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_200_OK)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
#دانش آموز با توجه به آی دی دعوت میتواند به دعوتش دسترسی داشته باشد آن را مدیریت یا حذف کند اما فیلد status در اینجا فقط باید قابل خواندن باشد
class detailMyInventationSend(APIView):
    permission_classes = (AllowAny,)
    serializer_class = InventationStudentSerializer
    def get_object(self,id):
        try:
            return CourseInvitation.objects.filter(id=id)
        except CourseInvitation.DoesNotExist:
            return None

    def get(self, request:Request, id):
        data=self.get_object(id)
        serializers=self.serializer_class(data,many=True)
        return Response(serializers.data or {'status':'دعوت مد نظر یافت نشد'}, status=status.HTTP_200_OK)
    def put(self, request:Request, id):
        data=self.get_object(id)
        serializers=self.serializer_class(data,data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_200_OK)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request:Request, id):
        data=CourseInvitation.objects.get(id=id)
        data.delete()

class InventationTecher(APIView):
    permission_classes = (AllowAny,)
    #permission_classes=(IsAuthenticated,)
    serializer_class = InventiationTeacherSerializer
    def post(self, request,id):

        serializer = self.serializer_class(data=request.data,context={'request': request,'id':id})
        if serializer.is_valid():

            serializer.save()
            teacher_id = serializer.data['teacher']
            teacher=CustomUser.objects.get(id=teacher_id)
            course = serializer.data['course_request']
            requestcourse=CourseRequest.objects.get(id=course)
            sender=requestcourse.Creator.id
            sender=CustomUser.objects.get(id=sender)
            Notificate=Notification.objects.create(user=teacher,sender=sender,title=f'تشکیل کلاس  {requestcourse.Title} ',description=f'{teacher}\n شما یک دعوت از طرف {sender}\n برای ایجاد کلاس {requestcourse.Title} دارید.عزیز:')
            Notificate.save()
            return Response({'status':f'دعوت از {teacher}با موفقیت انجام شد'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class HallWaiting(mixins.ListModelMixin,generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = HallWaitingSerializer
    queryset = WaitingHall.objects.filter(is_active=True)
    def get(self, request):
        return self.list(request)
class DetailRequset(generics.RetrieveAPIView):
    permission_classes = (AllowAny,)
    queryset = CourseRequest.objects
    serializer_class = DetailCourseRequestSerializer

class CreateProposalCourse(APIView):
    permission_classes = (AllowAny,)
    serializer_class = ProposalSerializer
    def user_object(self,request):
        user_custom = User.objects.filter(id=1).first()#آزمایشی بعدن تغییر کند
        return user_custom
    def course_object(self,id):
        course = CourseRequest.objects.get(id=id)
        return course

    def get(self,request,id):
        try:
            course = self.course_object(id)
            proposal = Proposal.objects.filter(course=course)
            serializer = self.serializer_class(proposal, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CourseRequest.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    def post(self,request,id:int):
        serializer=self.serializer_class(data=request.data,context={'request': request})
        try:
            course = self.course_object(id)
            user_custom = self.user_object(request)
            proposal = Proposal.objects.filter(course=course, user=user_custom).first()
            if serializer.is_valid():
                if (course.id == int(request.data['course'])):
                    if proposal is None:
                        serializer.save()
                        return Response({'status': 'پیشنهاد شما با موفقیت ثبت شد'}, status=status.HTTP_200_OK)
                    return Response({'status': 'شما قبلا برای این کلاس پیشنهاد داده اید'},
                                    status=status.HTTP_208_ALREADY_REPORTED)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except CourseRequest.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)




    # def put(self,request,id):
    #     course = self.course_object(id)
    #     user_custom=self.user_object(request)
    #     proposal=Proposal.objects.filter(course=course,user=user_custom).first()
    #     serializer=ProposalSerializer(proposal,data=request.data,context={'request': request})
    #     if serializer.is_valid():
    #         id_course=int(request.data['course'])
    #
    #         if id_course==id:
    #             serializer.save()
    #             return Response ({'status':'پیشنهاد شما با موفقیت تغییر کرد'},status=status.HTTP_200_OK)
    #         return Response(status=status.HTTP_403_FORBIDDEN)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #
    # def delete(self, request, id):
    #     try:
    #         course = self.course_object(id)
    #         user_custom = self.user_object(request)
    #
    #         proposal = Proposal.objects.filter(course=course,user=user_custom).first()
    #
    #
    #         if proposal is None:  # بررسی اینکه آیا پیشنهادی برای حذف وجود دارد
    #             return Response({'error': 'پیشنهادی برای حذف یافت نشد'}, status=status.HTTP_404_NOT_FOUND)
    #         proposal.delete()
    #         return Response({'status': 'پیشنهاد شما حذف شد'}, status=status.HTTP_200_OK)
    #
    #         # except course.DoesNotExist:
    #         #     return Response({'error': 'دوره موردنظر یافت نشد'}, status=status.HTTP_404_NOT_FOUND)
    #     except:
    #
    #         return Response(status=status.HTTP_404_NOT_FOUND)


class MySuggest(APIView):
    permission_classes = (AllowAny,)
    #permission_classes=(IsAuthenticated,)
    serializer_class = ProposalSerializer
    def get_user(self):
        #user_custom=User.objects.filter(id=request.data.get('user'))[0]
        user_custom = User.objects.filter(id=1)[0]
        return user_custom
    def get_proposal(self,id):
        proposal = Proposal.objects.get(id=id)
        return proposal
    def get(self,request,id):
        user=self.get_user()
        my_suggest=Proposal.objects.filter(user=user)
        serializer=self.serializer_class(my_suggest,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def put(self,request,id):
        my_suggest=self.get_proposal(id)
        user=self.get_user()
        if my_suggest is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            serializer=self.serializer_class(my_suggest,data=request.data,context={'request': request})
            if serializer.is_valid() :
                if user is not None and int(my_suggest.id)==id:
                    serializer.save()
                    return Response(data=serializer.data,status=status.HTTP_200_OK)
                return Response(status=status.HTTP_403_FORBIDDEN)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CreateCourse(APIView):
    permission_classes = (AllowAny,)
    serializer_class = CreateCourseSerializer
    def get(self,request):
        datacourse=CourseCreate.objects.all()
        serializer=self.serializer_class(datacourse,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    def post(self,request):
        serializer=self.serializer_class(data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def put(self,request,id):
        course=self.course_object(id)
        serializer=self.serializer_class(course,data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,id):
        course=self.course_object(id)
        course.delete()
        return Response(status=status.HTTP_200_OK)













# class ProposersRequest(APIView):
#     permission_classes = (AllowAny,)
#     # permission_classes=(IsAuthenticated,)
#     serializer_class = HallWaitingSerializer
#     course=waitingHall.objects.all()
#     def get(self, request,id:int):
#         course=get_objects(id)
#         if course:
#             return Response(course, status=status.HTTP_200_OK)
#         return Response({}, status=status.HTTP_404_NOT_FOUND)
#     def put(self, request,id:int):
#         course=get_objects(id)
#         if course:
#             serializer = self.serializer_class(course,data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data, status=status.HTTP_200_OK)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# class DetailRequest(APIView):
#     permission_classes = (AllowAny,)

# class CreateProposalCourse(APIView):
#     permission_classes = (AllowAny,)
#     # permission_classes=[IsAuthenticated]
#     serializer_class=ProposalSerializer
#     course=CourseRequest
#     def post(self, request):
#         idcourse=request.data.get('')
#         course=CourseRequest.get_objects(id=request.data['id'])
#         message=request.data['messages']
#         if Proposal.objects.filter(user=request.user, course=course).exists():
#             return Response({"error": "شما قبلاً برای این کلاس پیشنهاد داده‌اید."}, status=status.HTTP_400_BAD_REQUEST)
#         proposal = Proposal.objects.create(
#             user=request.user,  # کاربر لاگین‌شده
#             course=course,
#             message=message
#         )
#         proposal.save()
#         return Response({'add successfully'}, status=status.HTTP_200_OK)
#     def get(self, request,id):
#         course=Proposal.objects.get(id=id)
#         serializers = ProposalSerializer(course)
#         return Response(serializers.data)
# # class ListMyCourse(generics.ListAPIView):
# #     permission_classes = (AllowAny,)
# #     # permission_classes=[IsAuthenticated]
# #     serializer_class = ListCourseSerializer
# #     queryset = ListMyClasses.objects.all()
# #     def get(self, request):
# #         return self.list(request)
# # class DetailCourse(generics.RetrieveUpdateDestroyAPIView):
# #     permission_classes = (AllowAny,)
# #     # permission_classes=[IsAuthenticated]
# #     serializer_class = ListCourseSerializer
# #     queryset = ListMyClasses.objects.all()
# #     def get(self, request,pk:int):
# #         return self.retrieve(request,pk)
# #     def put(self,request,pk:int):
# #         return self.update(request,pk)
# #     def delete(self,request,pk:int):
# #         return self.destroy(request,pk)
#
# # class AcceptCourse(APIView):
# #     permission_classes = (AllowAny,)


