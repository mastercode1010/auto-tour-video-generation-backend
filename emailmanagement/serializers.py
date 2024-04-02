from rest_framework import serializers
from .models import ExitEmailSend

class ExitEmailSendSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExitEmailSend
        fields = ['id', 'customer', 'camera', 'wait_for_sec', 'from_email', 'text', 'date']
        
    def create(self, validated_data):
        return ExitEmailSend.objects.create(**validated_data)

    def update(self, instance, validated_data):

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance
