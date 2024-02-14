from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Header, Footer
from .serializers import HeaderSerializer, FooterSerializer
from rest_framework.permissions import IsAuthenticated
from user.permissions import IsAdmin
from django.core.files.storage import default_storage

class HeaderAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        headers = Header.objects.all()
        serializer = HeaderSerializer(headers, many=True)
        return Response({"status": True, "data": serializer.data}, status=status.HTTP_200_OK)

class HeaderAddAPIView(APIView):
    permission_classes = [IsAdmin]
    
    def post(self, request):
        serializer = HeaderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": True, "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"status": False, "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class HeaderDeleteAPIView(APIView):
    def post(self, request, *args, **kwargs):
        header_id = request.data.get('header_id')
        if not header_id:
            return Response({"status": False, "data": {"msg": "Header ID is required."}}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            header = Header.objects.get(pk=header_id)
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
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        footers = Footer.objects.all()
        serializer = FooterSerializer(footers, many=True)
        return Response({"status": True, "data": serializer.data}, status=status.HTTP_200_OK)

class FooterAddAPIView(APIView):
    permission_classes = [IsAdmin]
    
    def post(self, request):
        serializer = FooterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": True, "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"status": False, "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class FooterDeleteAPIView(APIView):
    def post(self, request, *args, **kwargs):
        footer_id = request.data.get('footer_id')
        if not footer_id:
            return Response({"status": False, "data": {"msg": "Footer ID is required."}}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            footer = Footer.objects.get(pk=footer_id)
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