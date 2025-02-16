from rest_framework import serializers

from classroom.models import  *
# from classroom.views import DetailRequest


class CreateRequestClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseRequest
        fields = '__all__'
    #     extra_kwargs = {
    #         'Creator': {'read_only': True}
    #     }
    # def create(self, validated_data):
    #     request = self.context.get('request')
    #     validated_data['Creator'] = request.user
    #     return super().create(validated_data) در نسخه اصلی اضافه شود


class HallWaitingSerializer(serializers.ModelSerializer):
    class Meta:
        model=WaitingHall
        fields='__all__'

class InventiationTeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model=CourseInvitation
        fields='__all__'
class ProposalSerializer(serializers.ModelSerializer):
    class Meta:
        model=Proposal
        fields='__all__'
    #     extra_kwargs = {
    #         'user':{'read_only':True},
    #     }
    # def create(self, validated_data):
    #     request = self.context.get('request')
    #     validated_data['user'] = request.user
    #     return super().create(validated_data)
# class ListCourseSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ListMyClasses
#         fields = '__all__'

# class ProposalSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Proposal
#         fields = '__all__'
# # class AcceptingSerializer(serializers.Serializer):
# #     requestsid=serializers
# #     waiting=HallWaiting
