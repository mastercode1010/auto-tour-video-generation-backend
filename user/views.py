from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import (
    UserRegistrationSerializer, 
    UserLoginSerializer, 
    PasswordResetRequestSerializer, 
    PasswordResetSerializer
)
from .models import User

class UserRegistrationAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        userdata = request.data
        userdata["street"] = userdata["street"] + '_' + userdata["city"] + '_' + userdata["state"] +  '_' + userdata["country"] + '_' + userdata["zipcode"]
        del userdata["city"]
        del userdata["state"]
        del userdata["country"]
        del userdata["zipcode"]
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": True, "data": "User registered successfully."}, status=201)
        return Response({"status": False, "data": serializer.errors}, status=400)

class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response({
                "status": True,
                "data": serializer.validated_data
            }, status=200)
        return Response({"status": False, "data": "Invalid email or password"}, status=400)

class PasswordResetRequestAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_link = request.build_absolute_uri(
                reverse('password_reset', kwargs={'uidb64': uidb64, 'token': token})
            )
            return Response({"status": "OK", "data": {"uidb64": uidb64, "token": token}})
        return Response(serializer.errors, status=400)

class PasswordResetAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, uidb64, token):
        serializer = PasswordResetSerializer(data={
            'uidb64': uidb64,
            'token': token,
            'new_password': request.data.get('new_password')
        })
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "OK", "message": "Password has been reset."})
        return Response(serializer.errors, status=400)