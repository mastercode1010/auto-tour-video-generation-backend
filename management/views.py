from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Header, Footer
from .serializers import HeaderSerializer, FooterSerializer
from rest_framework.permissions import IsAuthenticated
from user.permissions import IsAdmin, IsCustomer, IsAdminOrCustomer, IsOwnerOrAdmin, IsUserOrAdmin
from django.core.files.storage import default_storage
from rest_framework.parsers import MultiPartParser, FormParser

class HeaderAPIView(APIView):
    
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    
    def get_queryset(self):
        # print(self.request.user)
        if self.request.user.user_type == 1:
            return Header.objects.all()
        return Header.objects.filter(user=self.request.user)
    
    def get(self, request):
        headers = self.get_queryset()
        serializer = HeaderSerializer(headers, many=True)
        return Response({"status": True, "data": serializer.data}, status=status.HTTP_200_OK)

class HeaderAddAPIView(APIView):
    
    permission_classes = [IsAdminOrCustomer]
    parser_classes = (MultiPartParser, FormParser)
    
    def post(self, request):
        serializer = HeaderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"status": True, "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"status": False, "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class HeaderDeleteAPIView(APIView):
    
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAdminOrCustomer]
    
    def post(self, request, *args, **kwargs):
        header_id = request.data.get('header_id')
        if not header_id:
            return Response({"status": False, "data": {"msg": "Header ID is required."}}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            header = Header.objects.get(pk=header_id, user=request.user)
            # Delete associated video file
            if header.video_path:
                if default_storage.exists(header.video_path.name):
                    default_storage.delete(header.video_path.name)
            # Delete associated thumbnail file
            if header.thumbnail:
                if default_storage.exists(header.thumbnail.name):
                    default_storage.delete(header.thumbnail.name)
            header.delete()
            return Response({"status": True}, status=status.HTTP_200_OK)
        except Header.DoesNotExist:
            return Response({"status": False, "data": {"msg": "Header not found."}}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status": False, "data": {"msg": str(e)}}, status=status.HTTP_400_BAD_REQUEST)

class FooterAPIView(APIView):
    
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.user_type == 1:
            return Footer.objects.all()
        return Footer.objects.filter(user=self.request.user)
    
    def get(self, request):
        footers = self.get_queryset()
        serializer = FooterSerializer(footers, many=True)
        return Response({"status": True, "data": serializer.data}, status=status.HTTP_200_OK)

class FooterAddAPIView(APIView):
    
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAdminOrCustomer]
    
    def post(self, request):
        serializer = FooterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"status": True, "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"status": False, "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class FooterDeleteAPIView(APIView):
    
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAdminOrCustomer]
    
    def post(self, request, *args, **kwargs):
        footer_id = request.data.get('footer_id')
        if not footer_id:
            return Response({"status": False, "data": {"msg": "Footer ID is required."}}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            footer = Footer.objects.get(pk=footer_id, user=request.user)
            # Delete associated video file
            if footer.video_path:
                if default_storage.exists(footer.video_path.name):
                    default_storage.delete(footer.video_path.name)
            # Delete associated thumbnail file
            if footer.thumbnail:
                if default_storage.exists(footer.thumbnail.name):
                    default_storage.delete(footer.thumbnail.name)
            footer.delete()
            return Response({"status": True}, status=status.HTTP_200_OK)
        except Header.DoesNotExist:
            return Response({"status": False, "data": {"msg": "Footers not found."}}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status": False, "data": {"msg": str(e)}}, status=status.HTTP_400_BAD_REQUEST)