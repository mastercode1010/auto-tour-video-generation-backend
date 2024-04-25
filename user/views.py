from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import (
    UserRegistrationSerializer, 
    UserLoginSerializer, 
    PasswordResetRequestSerializer, 
    PasswordResetSerializer,
    UserUpdateSerializer,
    UserListSerializer,
    UserDetailSerializer,
)
from .models import User
from .permissions import IsAdmin
from rest_framework import status
from rest_framework.generics import ListAPIView
from django.shortcuts import get_object_or_404

class UserRegistrationAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        userdata = request.data
        userdata["street"] = userdata["street"] + '_' + userdata["city"] + '_' + userdata["state"] +  '_' + userdata["country"] + '_' + userdata["zipcode"]
        del userdata["city"]
        del userdata["state"]
        del userdata["country"]
        del userdata["zipcode"]
        serializer = UserRegistrationSerializer(data=userdata)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": True, "data": "User registered successfully."}, status=201)
        return Response({"status": False, "data": "email is already existed."}, status=400)

class UserDeleteAPIView(APIView):
    
    permission_classes = [IsAdmin]
    
    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({"status": False, "data": {"msg": "User ID is required."}}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(id=user_id)
            user.delete()
            return Response({"status": True}, status=status.HTTP_200_OK)
        except user.DoesNotExist:
            return Response({"status": False, "data": {"msg": "User not found."}}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status": False, "data": {"msg": str(e)}}, status=status.HTTP_400_BAD_REQUEST)

class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.validated_data['status']:
                # send_mail('Video Aggregation', 'Videolink: {"http://localhost:8000/media"/{output_file}}', settings.EMAIL_HOST_USER, ["codemaster9428@gmail.com"], fail_silently=False,)
                return Response({
                    "status": True,
                    "data": serializer.validated_data
                }, status=200)
            else:
                return Response({"status": False, "data": {"msg": "Please wait until admin allows you"}}, status=status.HTTP_423_LOCKED)
        return Response({"status": False, "data": {"msg": "Invalid email or password"}}, status=status.HTTP_406_NOT_ACCEPTABLE)

class UserUpdateAPIView(APIView):
    permission_classes = [IsAdmin]

    def post(self, request, *args, **kwargs):
        user_id = request.data['user_id']
        user = User.objects.get(id = user_id)
        userdata = request.data
        userdata["street"] = userdata["street"] + '_' + userdata["city"] + '_' + userdata["state"] +  '_' + userdata["country"] + '_' + userdata["zipcode"]
        del userdata["city"]
        del userdata["state"]
        del userdata["country"]
        del userdata["zipcode"]
        serializer = UserUpdateSerializer(user, data=userdata, partial=True)  # Allow partial update
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserRangeListAPIView(ListAPIView):
    serializer_class = UserListSerializer
    permission_classes = [IsAdmin]  # Assuming you want this endpoint to be protected

    def get_queryset(self):
        """
        Optionally restricts the returned users to a given range,
        by filtering against a `start_row_index` and `end_row_index` query parameter in the URL.
        """
        queryset = User.objects.all()
        start_row_index = self.request.query_params.get('start_row_index', None)
        end_row_index = self.request.query_params.get('end_row_index', None)

        if start_row_index is not None and end_row_index is not None:
            start_row_index = int(start_row_index)
            end_row_index = int(end_row_index)
            return queryset[start_row_index:end_row_index]
        return queryset

class GetUserByIdAPIView(APIView):
    permission_classes = [IsAdmin]  # Or adjust as per your security requirements

    def get(self, request, pk, format=None):
        user = get_object_or_404(User, pk=pk)
        serializer = UserDetailSerializer(user)
        return Response(serializer.data)

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