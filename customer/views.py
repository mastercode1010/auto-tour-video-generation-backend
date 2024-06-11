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
    ClientUpdateSerializer
)
from .models import Client
from user.permissions import IsCustomer, IsAdmin, IsAdminOrCustomer
from rest_framework import status
from rest_framework.generics import ListAPIView
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import QueryDict

# Create your views here.
class ClientRegistrationAPIView(APIView):
    permission_classes = [IsAdminOrCustomer]

    parser_classes = (MultiPartParser, FormParser)
    
    def post(self, request):
        data = request.data
        mutable_data = data.copy()
        mutable_data['customer'] = request.user.pk
        print(mutable_data)
        # data['customer'] = request.user.pk
        client_serializer = ClientSerializer(data=mutable_data)
        if client_serializer.is_valid():
            client_serializer.save()
            return Response({'status': 'success', 'data': client_serializer.data}, status=200)
        else:
            return Response(client_serializer.errors, status=400)
        
    def get(self, request):
        customer = request.user
        if customer is not None:
            if customer.user_type == 1:
                clients = Client.objects.all()
            elif customer.user_type == 2:
                clients = Client.objects.filter(customer=customer.pk)
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
            'children_name': request.data.get('children_name'),
            'rfid_tag': request.data.get('rfid_tag')
        }
        children_serializer = ChildrenSerializer(data=children_data)
        if children_serializer.is_valid():
            children_serializer.save()
            
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
    
    permission_classes = [IsCustomer]
    
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
    permission_classes = [IsCustomer]

    def post(self, request, *args, **kwargs):
        client_id = request.data['client_id']
        client = Client.objects.get(id = client_id)
        userdata = request.data
        serializer = ClientUpdateSerializer(client, data=userdata, partial=True)  # Allow partial update
        if serializer.is_valid():
            serializer.save()
            updated_client = [Client.objects.get(id=client_id)]
            client_serializer = ClientSerializer(updated_client, many=True)
            return Response({'status': True, 'data': client_serializer.data[0]})
        else:
            return Response({'status': False, 'error': serializer.error}, status=400)
        
class GetClientforVideoAPIView(APIView):
    permission_classes = [IsAdminOrCustomer]  # Or adjust as per your security requirements

    def get(self, request):
        customer = request.user
        if customer is not None:
            if customer.user_type == 1:
                return Response({'status': True, 'data': "You don't have any permission to see the client list."}, status=status.HTTP_403_FORBIDDEN)
            elif customer.user_type == 2:
                clients = Client.objects.filter(customer=customer.pk, paid_status = True, tour_status = False)
            serializer = ClientSerializer(clients, many=True)
            return Response({'status': True, 'data': serializer.data})
        else:
            return Response({'status': False, 'error': 'Customer ID is required'}, status=400)