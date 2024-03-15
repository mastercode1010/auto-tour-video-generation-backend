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
    ClientUpdateSerializer, 
    ClientPhotoSerializer,
    ChildrenPhotoSerializer
    # FacialPictureRegistrationSerializer,
)
from .models import Client, ClientFacialPictures, ChildFacialPictures, Children
from user.permissions import IsCustomer, IsAdmin, IsAdminOrCustomer
from rest_framework import status
from rest_framework.generics import ListAPIView
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser

# Create your views here.
class ClientRegistrationAPIView(APIView):
    permission_classes = [IsCustomer]

    parser_classes = (MultiPartParser, FormParser)
    
    def post(self, request):
        data = request.data
        print(data)
        client_serializer = ClientSerializer(data=data)
        if client_serializer.is_valid():
            client = client_serializer.save()
            index = 0
            for key in ['front_1_file', 'front_2_file', 'left_file', 'right_file']:
                image_data = {
                    'client': client.pk,
                    'img_url': request.FILES.get(key),
                    'side_key': index
                }
                index = index + 1
                image_serializer = ClientPhotoSerializer(data=image_data)
                if image_serializer.is_valid():
                    image_serializer.save()
                else:
                    msg = key + " mustn't be empty."
                    return Response({'status': False, 'data': msg}, status=400)

            return Response({'status': 'success', 'data': client_serializer.data}, status=200)
        else:
            return Response(client_serializer.errors, status=400)
        
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
    
    def post(self, request, *args, **kwargs):
        client_id = request.data.get('client_id')
        client = get_object_or_404(Client, pk=client_id)
        
        children_data = {
            'client': client.pk,
            'children_name': request.data.get('children_name')
        }
        children_serializer = ChildrenSerializer(data=children_data)
        # print(children_serializer.is_valid())
        if children_serializer.is_valid():
            child = children_serializer.save()
            index = 0
            for key in ['front_1_file', 'front_2_file', 'left_file', 'right_file']:
                print(child.id)
                image_data = {
                    'child': child.pk,
                    'img_url': request.FILES.get(key),
                    'side_key': index
                }
                index = index + 1
                image_serializer = ChildrenPhotoSerializer(data=image_data)
                if image_serializer.is_valid():
                    image_serializer.save()
                else:
                    msg = key + " mustn't be empty."
                    return Response({'status': False, 'data': msg}, status=400)

            return Response({'status': 'success', 'data': children_serializer.data}, status=200)
        else:
            return Response(children_serializer.errors, status=400)
        
class GetClientByIdAPIView(APIView):
    permission_classes = [IsAdminOrCustomer]  # Or adjust as per your security requirements

    def get(self, request, pk, format=None):
        client = get_object_or_404(Client, pk=pk)
        client_array = [client]
        client_serializer = ClientSerializer(client_array, many=True)
        return Response({'status': True, 'data': client_serializer.data[0]})
    
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

class ClientUpdateAPIView(APIView):
    permission_classes = [IsAdminOrCustomer]

    def post(self, request, *args, **kwargs):
        client_id = request.data['client_id']
        user = Client.objects.get(id = client_id)
        userdata = request.data
        # print(userdata)
        serializer = ClientUpdateSerializer(user, data=userdata, partial=True)  # Allow partial update
        if serializer.is_valid():
            serializer.save()
            updated_client = [Client.objects.get(id=client_id)]
            client_serializer = ClientSerializer(updated_client, many=True)
            return Response({'status': True, 'data': client_serializer.data[0]})
        else:
            return Response({'status': False, 'error': serializer.error}, status=400)