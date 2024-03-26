from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ColoringPage
from .serializers import ColoringPageSerializer
from user.permissions import IsAdminOrCustomer, IsCustomer

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
            coloring_pages = ColoringPage.objects.get(customer = user)
        serializer = ColoringPageSerializer(coloring_pages, many=True)
        length = serializer.data.__len__()
        data = []
        for i in range(length):
            sepdata = {
                "customer_id": serializer.data[i]['customer'],
                "camera_id": serializer.data[i]['camera'],
                "coloringpage": serializer.data[i]['coloringpage'],
                "wait_for_sec": serializer.data[i]['wait_for_sec'],
                "text": serializer.data[i]['text']
            }
            data.append(sepdata)

        return Response({'status': True, 'data': serializer.data})

    def post(self, request, format=None):
        # pagedata = request.data

        data = {
                "customer": request.data['customer_id'],
                "camera": request.data['camera_id'],
                "coloringpage": request.data['coloringpage'],
                "wait_for_sec": request.data['wait_for_sec'],
                "text": request.data['text']
            }

        serializer = ColoringPageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            data = {
                "id": serializer.data['id'],
                "customer_id": serializer.data['customer'],
                "camera_id": serializer.data['camera'],
                "coloringpage": serializer.data['coloringpage'],
                "wait_for_sec": serializer.data['wait_for_sec'],
                "text": serializer.data['text'],
                "date": serializer.data['date']
            }
            return Response({'status': True, 'data': data}, status=status.HTTP_201_CREATED)
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
        print(page)
        print(page.customer)
        print(user)
        if page.customer == user:
            serializer = ColoringPageSerializer(page)
            return Response(serializer.data)
        else:
            Response({'status': False, 'data': {'msg': "You don't have any permission of this data."}}, status=status.HTTP_403_FORBIDDEN)

    def post(self, request, format=None):
        user = request.user
        pk = request.data.get('id')
        page = self.get_object(pk)
        print(request.data)
        data = request.data
        mutabledata= data.copy()
        mutabledata['customer'] = mutabledata['customer_id']
        mutabledata['camera'] = mutabledata['camera_id']
        del mutabledata['customer_id']
        del mutabledata['camera_id']
        if page.customer == user:
            serializer = ColoringPageSerializer(instance=page, data=mutabledata)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
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