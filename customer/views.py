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
    ClientSerializer, 
    # ChildrenRegistrationSerializer, 
    # FacialPictureRegistrationSerializer,
)
from .models import Client, FacialPictures
from user.permissions import IsCustomer, IsAdmin
from rest_framework import status
from rest_framework.generics import ListAPIView
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import JsonResponse

# def facial_picture_scrap(clientdata, client_id, face_type = 0):
#     facial_picture_1 = {}
#     facial_picture_2 = {}
#     facial_picture_3 = {}
#     facial_picture_4 = {}
#     facial_picture_1["side_key"] = 1
#     facial_picture_2["side_key"] = 2
#     facial_picture_3["side_key"] = 3
#     facial_picture_4["side_key"] = 4
#     facial_picture_1["img_url"] = clientdata["front_1_file"]
#     facial_picture_2["img_url"] = clientdata["front_2_file"]
#     facial_picture_3["img_url"] = clientdata["left_file"]
#     facial_picture_4["img_url"] = clientdata["right_file"]
#     facial_picture_1["client_id"] = client_id
#     facial_picture_2["client_id"] = client_id
#     facial_picture_3["client_id"] = client_id
#     facial_picture_4["client_id"] = client_id
#     facial_picture_1["face_type"] = face_type
#     facial_picture_2["face_type"] = face_type
#     facial_picture_3["face_type"] = face_type
#     facial_picture_4["face_type"] = face_type
#     return facial_picture_1, facial_picture_2, facial_picture_3, facial_picture_4

# Create your views here.
class ClientRegistrationAPIView(APIView):
    permission_classes = [AllowAny]

    parser_classes = (MultiPartParser, FormParser)
    
    def post(self, request):
        data = request.data
        client_serializer = ClientSerializer(data=data)
        if client_serializer.is_valid():
            client = client_serializer.save()
            # Assuming files are sent as part of the request
            files = {
                'front_1': data.get('front_1_file'),
                'front_2': data.get('front_2_file'),
                'left': data.get('left_file'),
                'right': data.get('right_file')
            }
            for index, (key, file) in enumerate(files.items(), start=1):
                FacialPictures.objects.create(client_id=client.id, img_url=file, side_key=index, face_type=0)
            return JsonResponse({"status": True, "data": client_serializer.data})
        else:
            return JsonResponse({"status": False, "errors": client_serializer.errors}, status=400)