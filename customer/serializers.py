from rest_framework import serializers
from .models import Client, Children, FacialPictures
from rest_framework import serializers

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'