from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ExitEmailSend
from .serializers import ExitEmailSendSerializer
from user.permissions import IsAdminOrCustomer, IsCustomer
from management.models import Camera
from user.models import User
from django.core.files.storage import default_storage

class ExitEmailSendListCreateAPIView(APIView):
    """
    List all coloring pages, or create a new coloring page.
    """
    permission_classes = [IsAdminOrCustomer]

    def get(self, request, format=None):
        user = request.user
        if user.user_type == 1:
            exitemailsend = ExitEmailSend.objects.all()
        elif user.user_type == 2:
            exitemailsend = ExitEmailSend.objects.filter(customer = user)
        serializer = ExitEmailSendSerializer(exitemailsend, many=True)
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
                "wait_for_sec": serializer.data[i]['wait_for_sec'],
                "text": serializer.data[i]['text'],
                "from_email": serializer.data[i]['from_email'],
                "date": serializer.data[i]['date']
            }
            data.append(sepdata)

        return Response({'status': True, 'data': data})

    def post(self, request, format=None):
        user = request.user
        data = {
                "customer": user.pk,
                "camera": request.data['camera_id'],
                "wait_for_sec": request.data['wait_for_sec'],
                "from_email": request.data['from_email'],
                "text": request.data['text']
            }

        serializer = ExitEmailSendSerializer(data=data)
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
                "wait_for_sec": serializer.data['wait_for_sec'],
                "text": serializer.data['text'],
                "from_email": serializer.data['from_email'],
                "date": serializer.data['date']
            }
            return Response({'status': True, 'data': sepdata}, status=status.HTTP_201_CREATED)
        return Response({'status': True, 'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class ExitEmailSendDetailAPIView(APIView):
    """
    Retrieve, update, or delete a coloring page instance.
    """

    permission_classes = [IsAdminOrCustomer]

    def get_object(self, pk):
        try:
            return ExitEmailSend.objects.get(pk=pk)
        except ExitEmailSend.DoesNotExist:
            return Response({'status': False, 'data': 'No data exists.'}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        user = request.user
        exitdata = self.get_object(pk)
        serializer = ExitEmailSendSerializer(exitdata)
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
            "wait_for_sec": serializer.data['wait_for_sec'],
            "text": serializer.data['text'],
            "from_email": serializer.data['from_email'],
            "date": serializer.data['date']
        }
        return Response({'status': True, 'data': sepdata}, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        user = request.user
        pk = request.data.get('id')
        exitdata = self.get_object(pk)
        print(exitdata)
        data = request.data
        mutabledata= data.copy()
        mutabledata['customer'] = user.pk
        mutabledata['camera'] = mutabledata['camera_id']
        del mutabledata['camera_id']
        if exitdata.customer == user:
            serializer = ExitEmailSendSerializer(instance=exitdata, data=mutabledata)
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
                    "wait_for_sec": serializer.data['wait_for_sec'],
                    "text": serializer.data['text'],
                    "from_email": serializer.data['from_email'],
                    "date": serializer.data['date']
                }
                return Response({'status': True, 'data': sepdata}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'status': False, 'data': {'msg': "You don't have any permission of this data."}}, status=status.HTTP_403_FORBIDDEN)

class ExitEmailSendDeleteAPIView(APIView):

    permission_classes = [IsAdminOrCustomer]

    def get_object(self, pk):
        try:
            return ExitEmailSend.objects.get(pk=pk)
        except ExitEmailSend.DoesNotExist:
            return Response({'status': False, 'data': 'No data exists.'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, format=None):
        user = request.user
        pk = request.data.get('id')
        exitemailsend = self.get_object(pk)
        if exitemailsend.customer == user:
            exitemailsend.delete()
            return Response({"status": True, "data": {"id": pk}}, status=status.HTTP_200_OK)
        else:
            return Response({'status': False, 'data': {'msg': "You don't have any permission of this data."}}, status=status.HTTP_403_FORBIDDEN)