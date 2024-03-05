from rest_framework import serializers
from .models import Client, Children, FacialPictures
from rest_framework import serializers

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacialPictures
        fields = ('img_url', 'side_key')

class ChildrenSerializer(serializers.ModelSerializer):
    photos = serializers.SerializerMethodField()

    class Meta:
        model = Children
        fields = ['id', 'client_id', 'children_name', 'date', 'photos']

    def get_photos(self, obj):
        photos = FacialPictures.objects.filter(client_id=obj.id, face_type=1)
        return PhotoSerializer(photos, many=True).data


class ClientSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    photos = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = ['id', 'customer_id', 'client_name', 'client_email', 'get_same_video', 'appears_in_other_video', 'voice_can_be_recorded', 'be_shown_potential', 'be_shown_public_business', 'be_shown_social_media', 'date', 'children', 'photos']

    def get_children(self, obj):
        children = Children.objects.filter(client_id=obj.id)
        return ChildrenSerializer(children, many=True).data

    def get_photos(self, obj):
        photos = FacialPictures.objects.filter(client_id=obj.id, face_type=0)
        return PhotoSerializer(photos, many=True).data
