from rest_framework import serializers
from .models import Client, Children
from rest_framework import serializers

class ChildrenSerializer(serializers.ModelSerializer):

    class Meta:
        model = Children
        fields = ['id', 'client', 'children_name', 'rfid_tag', 'date']


class ClientSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = ['id', 'customer', 'client_name', 'client_email', 'get_same_video', 'appears_in_others_video', 'voice_can_be_recorded', 'be_shown_potential', 'be_shown_public_business', 'be_shown_social_media', 'date', 'children', 'rfid_tag', 'tour_status', 'paid_status']

    def get_children(self, obj):
        children = Children.objects.filter(client_id=obj.id)
        return ChildrenSerializer(children, many=True).data
    

class ClientDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        exclude = ()  # Exclude password from the serialized data
        
class ClientUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('id', 'client_name', 'client_email', 'get_same_video', 'appears_in_others_video', 'voice_can_be_recorded', 'rfid_tag', 'be_shown_potential', 'be_shown_public_business', 'be_shown_social_media', 'date')

    def update(self, instance, validated_data):
        instance.client_name = validated_data.get('client_name', instance.client_name)
        instance.client_email = validated_data.get('client_email', instance.client_email)
        instance.get_same_video = validated_data.get('get_same_video', instance.get_same_video)
        instance.appears_in_others_video = validated_data.get('appears_in_others_video', instance.appears_in_others_video)
        instance.voice_can_be_recorded = validated_data.get('voice_can_be_recorded', instance.voice_can_be_recorded)
        instance.be_shown_potential = validated_data.get('be_shown_potential', instance.be_shown_potential)
        instance.be_shown_public_business = validated_data.get('be_shown_public_business', instance.be_shown_public_business)
        instance.be_shown_social_media = validated_data.get('be_shown_social_media', instance.be_shown_social_media)
        instance.rfid_tag = validated_data.get('rfid_tag', instance.rfid_tag)
        instance.tour_status = validated_data.get('tour_status', instance.tour_status)
        instance.paid_status = validated_data.get('paid_status', instance.paid_status)
        instance.save()
        return instance
