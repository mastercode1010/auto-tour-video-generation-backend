from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ColoringPage
from .serializers import ColoringPageSerializer
from user.permissions import IsAdminOrCustomer, IsCustomer
from management.models import Camera
from user.models import User
from django.core.mail import EmailMessage
from django.core.files.storage import default_storage
from customer.models import Client
from customer.serializers import ClientSerializer
from django.conf import settings
import os

class ColoringPageListCreateAPIView(APIView):
    """
    List all coloring pages, or create a new coloring page.
    """
    permission_classes = [IsAdminOrCustomer]

    def get(self, request, format=None):
        user = request.user
        if user.user_type == 1:
            coloring_pages = ColoringPage.objects.all()
        elif user.user_type == 2:
            coloring_pages = ColoringPage.objects.filter(customer = user)
        serializer = ColoringPageSerializer(coloring_pages, many=True)
        length = serializer.data.__len__()
        data = []
        for i in range(length):
            customer = User.objects.get(pk=serializer.data[i]['customer'])
            camera = Camera.objects.get(pk=serializer.data[i]['camera'])
            sepdata = {
                "id": serializer.data[i]['id'],
                "customer_data": {
                    "id": customer.id,
                    "username": customer.username
                },
                "camera": {
                    "id": camera.id,
                    "camera_name": camera.camera_name,
                },
                "coloringpage": serializer.data[i]['coloringpage'],
                "wait_for_sec": serializer.data[i]['wait_for_sec'],
                "text": serializer.data[i]['text'],
                "date": serializer.data[i]['date']
            }
            data.append(sepdata)

        return Response({'status': True, 'data': data})

    def post(self, request, format=None):
        user = request.user
        data = {
                "customer": user.pk,
                "camera": request.data['camera_id'],
                "coloringpage": request.data['coloringpage'],
                "wait_for_sec": request.data['wait_for_sec'],
                "text": request.data['text']
            }

        serializer = ColoringPageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            customer = User.objects.get(pk=serializer.data['customer'])
            camera = Camera.objects.get(pk=serializer.data['camera'])
            sepdata = {
                "id": serializer.data['id'],
                "customer_data": {
                    "id": customer.id,
                    "username": customer.username
                },
                "camera": {
                    "id": camera.id,
                    "camera_name": camera.camera_name,
                },
                "coloringpage": serializer.data['coloringpage'],
                "wait_for_sec": serializer.data['wait_for_sec'],
                "text": serializer.data['text'],
                "date": serializer.data['date']
            }
            return Response({'status': True, 'data': sepdata}, status=status.HTTP_201_CREATED)
        return Response({'status': True, 'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class ColoringPageDetailAPIView(APIView):
    """
    Retrieve, update, or delete a coloring page instance.
    """

    permission_classes = [IsAdminOrCustomer]

    def get_object(self, pk):
        try:
            return ColoringPage.objects.get(pk=pk)
        except ColoringPage.DoesNotExist:
            return Response({'status': False, 'data': 'No data exists.'}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        user = request.user
        page = self.get_object(pk)
        serializer = ColoringPageSerializer(page)
        customer = User.objects.get(pk=serializer.data['customer'])
        camera = Camera.objects.get(pk=serializer.data['camera'])
        sepdata = {
            "id": serializer.data['id'],
            "customer_data": {
                "id": customer.id,
                "username": customer.username
            },
            "camera": {
                "id": camera.id,
                "camera_name": camera.camera_name,
            },
            "coloringpage": serializer.data['coloringpage'],
            "wait_for_sec": serializer.data['wait_for_sec'],
            "text": serializer.data['text'],
            "date": serializer.data['date']
        }
        return Response({'status': True, 'data': sepdata}, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        user = request.user
        pk = request.data.get('id')
        page = self.get_object(pk)
        data = request.data
        mutabledata= data.copy()
        mutabledata['customer'] = user.pk
        mutabledata['camera'] = mutabledata['camera_id']
        del mutabledata['camera_id']
        print(mutabledata)
        print(page.customer == user)
        if page.customer == user:
            serializer = ColoringPageSerializer(instance=page, data=mutabledata)
            if serializer.is_valid():
                serializer.save()
                customer = User.objects.get(pk=serializer.data['customer'])
                camera = Camera.objects.get(pk=serializer.data['camera'])
                sepdata = {
                    "id": serializer.data['id'],
                    "customer_data": {
                        "id": customer.id,
                        "username": customer.username
                    },
                    "camera": {
                        "id": camera.id,
                        "camera_name": camera.camera_name,
                    },
                    "coloringpage": serializer.data['coloringpage'],
                    "wait_for_sec": serializer.data['wait_for_sec'],
                    "text": serializer.data['text'],
                    "date": serializer.data['date']
                }
                return Response({'status': True, 'data': sepdata}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'status': False, 'data': {'msg': "You don't have any permission of this data."}}, status=status.HTTP_403_FORBIDDEN)

class ColoringPageDeleteAPIView(APIView):

    permission_classes = [IsAdminOrCustomer]

    def get_object(self, pk):
        try:
            return ColoringPage.objects.get(pk=pk)
        except ColoringPage.DoesNotExist:
            return Response({'status': False, 'data': 'No data exists.'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, format=None):
        user = request.user
        pk = request.data.get('id')
        coloring_page = self.get_object(pk)
        if coloring_page.customer == user:
            if coloring_page.coloringpage:
                pageurl = str(coloring_page.coloringpage)
                if default_storage.exists(pageurl):
                    default_storage.delete(pageurl)
            coloring_page.delete()
            return Response({"status": True, "data": {"id": pk}}, status=status.HTTP_200_OK)
        else:
            return Response({'status': False, 'data': {'msg': "You don't have any permission of this data."}}, status=status.HTTP_403_FORBIDDEN)
        
class SendColoringPage(APIView):
    def post(self, request, *args, **kwargs):
        user = request.user
        camera_id = request.data.get('camera_id')
        camera = Camera.objects.get(pk = camera_id)
        # print(camera)
        coloring_page = ColoringPage.objects.get(camera = camera, customer = user)
        serializer = ColoringPageSerializer(coloring_page)
        # print(serializer)
        coloring_page = serializer.data
        clients = Client.objects.filter(customer = request.user, paid_status = True, tour_status = False)
        client_list = ClientSerializer(clients, many=True)
        # print(client_list.data[0]['client_email'])
        email_list = []
        for client in client_list.data:
            email_list.append(client['client_email'])
        if len(email_list) > 0:
            email_message = EmailMessage(
                subject='ColoringPage',
                body='This is my coloring page.',
                from_email='otis1880town@gmail.com',
                to=email_list,
            )
            # print(settings.STATIC_ROOT)
            STATIC_ROOT = settings.STATIC_ROOT
            print(STATIC_ROOT)
            relative_path = coloring_page['coloringpage'].lstrip('/\\')
            coloringpage_path = os.path.join(STATIC_ROOT, relative_path)
            print(coloringpage_path)
            email_message.attach_file(coloringpage_path)
            email_message.send()
            return Response({'status': 'Coloring page sent successfully.'}, status=status.HTTP_200_OK)
        return Response({'error': "There isn't any paid client."}, status=status.HTTP_400_BAD_REQUEST)