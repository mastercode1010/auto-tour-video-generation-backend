from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers

class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for registering a new user.
    """
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'confirm_password', 'phone_number', 'street', 'user_type', 'user_avatar', 'contact_email', 'contact_name', 'contact_phone_number')
        extra_kwargs = {'password': {'write_only': True}}
    
    def validate(self, data):
        # Ensure the passwords are the same
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(**validated_data)
        return user
    
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'phone_number', 'street', 'user_avatar', 'contact_email', 'contact_name', 'contact_phone_number')

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.street = validated_data.get('street', instance.street)
        instance.user_avatar = validated_data.get('user_avatar', instance.user_avatar)
        instance.contact_email = validated_data.get('contact_email', instance.contact_email)
        instance.contact_name = validated_data.get('contact_name', instance.contact_name)
        instance.contact_phone_number = validated_data.get('contact_phone_number', instance.contact_phone_number)
        instance.save()
        return instance

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone_number', 'street', 'user_type', 'user_avatar', 'contact_email', 'contact_name', 'contact_phone_number']  # Exclude 'password'
        read_only_fields = fields

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if user and user.is_active:
            refresh = RefreshToken.for_user(user)
            access = refresh.access_token

            return {
                'refresh': str(refresh),
                'access': str(access),
                'user_id': user.id,
                'user_type': user.user_type,
                'username': user.username,
            }
        else:
            raise serializers.ValidationError("Invalid email or password")
        
class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        # Validate if user exists in database
        try:
            User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")
        return value

class PasswordResetSerializer(serializers.Serializer):
    uidb64 = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)

    def validate(self, data):
        try:
            uid = force_str(urlsafe_base64_decode(data['uidb64']))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, data['token']):
            return data
        else:
            raise serializers.ValidationError('The reset link is invalid or has expired.')

    def save(self, **kwargs):
        uid = force_str(urlsafe_base64_decode(self.validated_data['uidb64']))
        user = User.objects.get(pk=uid)
        user.set_password(self.validated_data['new_password'])
        user.save()