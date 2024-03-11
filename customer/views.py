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
    ChildrenSerializer,
    ClientDetailSerializer, 
    # FacialPictureRegistrationSerializer,
)
from .models import Client, FacialPictures
from user.permissions import IsCustomer, IsAdmin, IsAdminOrCustomer
from rest_framework import status
from rest_framework.generics import ListAPIView
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import JsonResponse

# Create your views here.
class ClientRegistrationAPIView(APIView):
    permission_classes = [IsCustomer]

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
        
    def get(self, request):
        customer_id = request.query_params.get('customer_id')
        if customer_id is not None:
            clients = Client.objects.filter(customer_id=customer_id)
            serializer = ClientSerializer(clients, many=True)
            return Response({'status': True, 'data': serializer.data})
        else:
            return Response({'status': False, 'error': 'Customer ID is required'}, status=400)

class ChildrenRegistrationAPIView(APIView):
    permission_classes = [IsCustomer]

    parser_classes = (MultiPartParser, FormParser)
    
    def post(self, request):
        children_serializer = ChildrenSerializer(data=request.data)
        if children_serializer.is_valid():
            child = children_serializer.save()
            
            files = {
                'front_1_file': request.FILES.get('front_1_file'),
                'front_2_file': request.FILES.get('front_2_file'),
                'left_file': request.FILES.get('left_file'),
                'right_file': request.FILES.get('right_file'),
            }
            side_keys = [1, 2, 3, 4]
            
            for file_key, side_key in zip(files.keys(), side_keys):
                if files[file_key]:
                    FacialPictures.objects.create(
                        client_id=child.id,  # Assuming this refers correctly to the child id for face_type = 1
                        img_url=files[file_key],
                        side_key=side_key,
                        face_type=1,  # As specified, always 1 for this API
                        date=child.date  # Using the date from the child object
                    )
                    
            return JsonResponse({'status': 'success', 'message': 'Child and photos added successfully'}, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse({'status': 'error', 'errors': children_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
class GetClientByIdAPIView(APIView):
    permission_classes = [IsAdminOrCustomer]  # Or adjust as per your security requirements

    def get(self, request, pk, format=None):
        try:
            client = Client.objects.get(pk=pk)
            serializer = ClientDetailSerializer(client)
            return Response({'status': True, 'data': serializer.data})
        except Client.DoesNotExist:
            return Response({'status': False})
    
class ClientDeleteAPIView(APIView):
    
    permission_classes = [IsAdminOrCustomer]
    
    def post(self, request, *args, **kwargs):
        client_id = request.data.get('client_id')
        if not client_id:
            return Response({"status": False, "data": {"msg": "Client ID is required."}}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            client = Client.objects.get(id=client_id)
            
            client.delete()
            return Response({"status": True}, status=status.HTTP_200_OK)
        except client.DoesNotExist:
            return Response({"status": False, "data": {"msg": "Client not found."}}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status": False, "data": {"msg": str(e)}}, status=status.HTTP_400_BAD_REQUEST)
