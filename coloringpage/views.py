from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ColoringPage
from .serializers import ColoringPageSerializer
from user.permissions import IsAdminOrCustomer, IsCustomer
from management.models import Camera
from user.models import User

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
                "customer_data": {
                    "id": customer.id,
                    "username": customer.username
                },
                "camera": {
                    "id": camera.id,
                    "camera_seq_number": camera.camera_seq_number,
                    "camera_name": camera.camera_name,
                    "camera_type": camera.camera_type
                },
                "coloringpage": serializer.data[i]['coloringpage'],
                "wait_for_sec": serializer.data[i]['wait_for_sec'],
                "text": serializer.data[i]['text'],
                "date": serializer.data[i]['date']
            }
            data.append(sepdata)

        return Response({'status': True, 'data': data})

    def post(self, request, format=None):
        # pagedata = request.data
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
                "customer_data": {
                    "id": customer.id,
                    "username": customer.username
                },
                "camera": {
                    "id": camera.id,
                    "camera_seq_number": camera.camera_seq_number,
                    "camera_name": camera.camera_name,
                    "camera_type": camera.camera_type
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
        if page.customer == user:
            serializer = ColoringPageSerializer(page)
            customer = User.objects.get(pk=serializer.data['customer'])
            camera = Camera.objects.get(pk=serializer.data['camera'])
            sepdata = {
                "customer_data": {
                    "id": customer.id,
                    "username": customer.username
                },
                "camera": {
                    "id": camera.id,
                    "camera_seq_number": camera.camera_seq_number,
                    "camera_name": camera.camera_name,
                    "camera_type": camera.camera_type
                },
                "coloringpage": serializer.data['coloringpage'],
                "wait_for_sec": serializer.data['wait_for_sec'],
                "text": serializer.data['text'],
                "date": serializer.data['date']
            }
            return Response({'status': True, 'data': sepdata}, status=status.HTTP_200_OK)
        else:
            Response({'status': False, 'data': {'msg': "You don't have any permission of this data."}}, status=status.HTTP_403_FORBIDDEN)

    def post(self, request, format=None):
        user = request.user
        pk = request.data.get('id')
        page = self.get_object(pk)
        print(request.data)
        data = request.data
        mutabledata= data.copy()
        mutabledata['customer'] = user.pk
        mutabledata['camera'] = mutabledata['camera_id']
        del mutabledata['camera_id']
        if page.customer == user:
            serializer = ColoringPageSerializer(instance=page, data=mutabledata)
            if serializer.is_valid():
                serializer.save()
                customer = User.objects.get(pk=serializer.data['customer'])
                camera = Camera.objects.get(pk=serializer.data['camera'])
                sepdata = {
                    "customer_data": {
                        "id": customer.id,
                        "username": customer.username
                    },
                    "camera": {
                        "id": camera.id,
                        "camera_seq_number": camera.camera_seq_number,
                        "camera_name": camera.camera_name,
                        "camera_type": camera.camera_type
                    },
                    "coloringpage": serializer.data['coloringpage'],
                    "wait_for_sec": serializer.data['wait_for_sec'],
                    "text": serializer.data['text'],
                    "date": serializer.data['date']
                }
                return Response({'status': True, 'data': sepdata}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            Response({'status': False, 'data': {'msg': "You don't have any permission of this data."}}, status=status.HTTP_403_FORBIDDEN)

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
            coloring_page.delete()
            return Response({'status': True, 'data': 'Successfully deleted.'}, status=status.HTTP_204_NO_CONTENT)
        else:
            Response({'status': False, 'data': {'msg': "You don't have any permission of this data."}}, status=status.HTTP_403_FORBIDDEN)