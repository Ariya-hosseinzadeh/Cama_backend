from rest_framework import serializers

from complaint_ticket.models import Complaint


class ComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = '__all__'
        extra_kwargs = {
                'user':{'read_only':True},
            }
        def create(self, validated_data):
            request = self.context.get('request')
            validated_data['user'] = request.user
            return super().create(validated_data)