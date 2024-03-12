from rest_framework import serializers
from .models import Client, Children, ClientFacialPictures, ChildFacialPictures
from rest_framework import serializers

class ClientPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientFacialPictures
        fields = ('img_url', 'side_key', 'client')

class ChildrenPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChildFacialPictures
        fields = ('img_url', 'side_key', 'child')

class ChildrenSerializer(serializers.ModelSerializer):
    photos = serializers.SerializerMethodField()

    class Meta:
        model = Children
        fields = ['id', 'client', 'children_name', 'date', 'photos']

    def get_photos(self, obj):
        photos = ChildFacialPictures.objects.filter(child_id=obj.id, face_type=1)
        return ChildrenPhotoSerializer(photos, many=True).data


class ClientSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    photos = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = ['id', 'customer_id', 'client_name', 'client_email', 'get_same_video', 'appears_in_others_video', 'voice_can_be_recorded', 'be_shown_potential', 'be_shown_public_business', 'be_shown_social_media', 'date', 'children', 'photos']

    def get_children(self, obj):
        children = Children.objects.filter(client_id=obj.id)
        return ChildrenSerializer(children, many=True).data

    def get_photos(self, obj):
        photos = ClientFacialPictures.objects.filter(client_id=obj.id, face_type=0)
        return ClientPhotoSerializer(photos, many=True).data


class ClientDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        exclude = ()  # Exclude password from the serialized data
        
class ClientUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('id', 'client_name', 'client_email', 'get_same_video', 'appears_in_others_video', 'voice_can_be_recorded', 'be_shown_potential', 'be_shown_public_business', 'be_shown_social_media', 'date')

    def update(self, instance, validated_data):
        instance.client_name = validated_data.get('client_name', instance.client_name)
        instance.client_email = validated_data.get('client_email', instance.client_email)
        instance.get_same_video = validated_data.get('get_same_video', instance.get_same_video)
        instance.appears_in_others_video = validated_data.get('appears_in_others_video', instance.appears_in_others_video)
        instance.voice_can_be_recorded = validated_data.get('voice_can_be_recorded', instance.voice_can_be_recorded)
        instance.be_shown_potential = validated_data.get('be_shown_potential', instance.be_shown_potential)
        instance.be_shown_public_business = validated_data.get('be_shown_public_business', instance.be_shown_public_business)
        instance.be_shown_social_media = validated_data.get('be_shown_social_media', instance.be_shown_social_media)
        # print(instance)
        instance.save()
        return instance
