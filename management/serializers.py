from rest_framework import serializers
from .models import Header, Footer, CameraVoice, Camera, Video

class CameraSerializer(serializers.ModelSerializer):

    class Meta:
        model = Camera
        fields = ['id', 'camera_name', 'camera_user_name', 'camera_ip', 'camera_port', 'password', 'created_at', 'updated_at']
    
    def validate(self, attrs):
        if self.instance:
            return attrs

        camera_ip = attrs.get('camera_ip')
        camera_port = attrs.get('camera_port')
        if Camera.objects.filter(camera_ip=camera_ip, camera_port=camera_port).exists():
            raise serializers.ValidationError("A camera with this IP address and port already exists.")
        return super().validate(attrs)

class HeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Header
        fields = ['id', 'video_path', 'created_at', 'updated_at', 'thumbnail']
        read_only_fields = ['thumbnail']  # Make 'thumbnail' field read-only

    def create(self, validated_data):
        # Create a new Header instance using the validated data.
        header_instance = Header.objects.create(**validated_data)
        return header_instance

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'video_path', 'created_at', 'updated_at', 'thumbnail']
        read_only_fields = ['thumbnail']  # Make 'thumbnail' field read-only

    def create(self, validated_data):
        # Create a new Header instance using the validated data.
        video_instance = Video.objects.create(**validated_data)
        return video_instance

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance


class FooterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Footer
        fields = ['id', 'video_path', 'created_at', 'updated_at', 'thumbnail']
        read_only_fields = ['thumbnail']  # Make 'thumbnail' field read-only

    def create(self, validated_data):
        # Create a new footer instance using the validated data.
        footer_instance = Footer.objects.create(**validated_data)
        return footer_instance

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance

class CameraVoiceSerializer(serializers.ModelSerializer):
    
    camera_id = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CameraVoice
        fields = ['id', 'customer', 'customer_id', 'camera', 'camera_id', 'wait_for_sec', 'enter_or_exit_code', 'text', 'date']
        extra_kwargs = {
            'camera': {'write_only': True},
            'customer': {'write_only': True}
        }

    def get_camera_id(self, obj):
        return obj.camera.pk
    def get_customer_id(self, obj):
        return obj.customer.pk
    
    def update(self, instance, validated_data):
        instance.customer = validated_data.get('customer', instance.customer)
        instance.camera = validated_data.get('camera', instance.camera)
        instance.wait_for_sec = validated_data.get('wait_for_sec', instance.wait_for_sec)
        instance.enter_or_exit_code = validated_data.get('enter_or_exit_code', instance.enter_or_exit_code)
        instance.text = validated_data.get('text', instance.text)
        instance.save()
        return instance
        