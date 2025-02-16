from rest_framework import serializers
from classroom.models import *
from complaint_ticket.models import *
from user_custom.models import *

class MyRequestCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseRequest
        fields = '__all__'
        #extra_kwargs = {
        #         'user':{'read_only':True},
        #     }
        # def create(self, validated_data):
        #     request = self.context.get('request')
        #     validated_data['user'] = request.user
        #     return super().create(validated_data)
class MyCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'
        # extra_kwargs = {
        #         'user':{'read_only':True},
        #     }
        # def create(self, validated_data):
        #     request = self.context.get('request')
        #     validated_data['user'] = request.user
        #     return super().create(validated_data)
class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
        # extra_kwargs = {
        #         'user':{'read_only':True},
        #     }
        # def create(self, validated_data):
        #     request = self.context.get('request')
        #     validated_data['user'] = request.user
        #     return super().create(validated_data)
class MyComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = '__all__'
        # extra_kwargs = {
        #         'user':{'read_only':True},
        #     }
        # def create(self, validated_data):
        #     request = self.context.get('request')
        #     validated_data['user'] = request.user
        #     return super().create(validated_data)
class MyAdditionalInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model =AdditionalInformationUser
        fields = '__all__'
        # extra_kwargs = {
        #         'user':{'read_only':True},
        #     }
        # def create(self, validated_data):
        #     request = self.context.get('request')
        #     validated_data['user'] = request.user
        #     return super().create(validated_data)
