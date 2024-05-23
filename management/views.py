from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Header, Footer, Camera, CameraVoice
from .serializers import HeaderSerializer, FooterSerializer, CameraVoiceSerializer, CameraSerializer
from rest_framework.permissions import IsAuthenticated
from user.permissions import IsAdmin, IsCustomer, IsAdminOrCustomer, IsOwnerOrAdmin, IsUserOrAdmin
from django.core.files.storage import default_storage
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.http import JsonResponse
from user.models import User

class CameraAPIView(APIView):
    permission_classes = [IsAdminOrCustomer]
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request):
        customer = request.user
        if customer is not None:
            cameras = Camera.objects.filter(customer=customer.pk)
            serializer = CameraSerializer(cameras, many=True)
            return Response({'status': True, 'data': serializer.data})
        else:
            return Response({'status': False, 'error': 'You have to login in this site.'}, status=400)
        
    def post(self, request):
        serializer = CameraSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(customer = request.user)
            return Response({"status": True, "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"status": False, "data": {"msg": serializer.errors["non_field_errors"][0]}}, status=status.HTTP_400_BAD_REQUEST)
    
class CameraUpdateAPIView(APIView):
    permission_classes = [IsAdminOrCustomer]
    parser_classes = (MultiPartParser, FormParser)
    
    def get(self, request):
        customer = request.user
        camera_id = request.data.get('id')
        if customer is not None:
            camera = Camera.objects.get(customer=customer.pk, id = camera_id)
            serializer = CameraSerializer(camera)
            return Response({'status': True, 'data': serializer.data})
        else:
            return Response({'status': False, 'error': 'You have to login in this site.'}, status=400)

    def post(self, request):
        camera_id = request.data.get('id')
        customer = request.user
        try:
            camera = Camera.objects.get(id=camera_id, customer=request.user)
            data = request.data
            data = {
                "camera_name": data.get("camera_name"),
                "camera_ip": data.get("camera_ip"),
                "camera_port": data.get("camera_port"),
                "password": data.get("password"),
                "camera_user_name": data.get("camera_user_name")
            }
            serializer = CameraSerializer(camera, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"status": True, "data": serializer.data}, status=status.HTTP_200_OK)
            return Response({"status": False, "data": {"msg": serializer.errors}})
        except Camera.DoesNotExist:
            try:
                camera_existence = Camera.objects.get(id = camera_id)
                return Response({"status": False, "data": {"msg": "You don't have permission to delete this camera."}}, status=status.HTTP_403_FORBIDDEN)
            except Camera.DoesNotExist:
                return Response({"status": False, "data": {"msg": "Camera not found."}}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status": False, "data": {"msg": str(e)}}, status=status.HTTP_400_BAD_REQUEST)
    
class CameraDeleteAPIView(APIView):
    permission_classes = [IsAdminOrCustomer]
    parser_classes = (MultiPartParser, FormParser)
    
    def post(self, request):
        camera_id = request.data.get('id')
        if not camera_id:
            return Response({"status": False, "data": {"msg": "Header ID is required."}}, status=status.HTTP_400_BAD_REQUEST)
        try:
            camera = Camera.objects.get(id=camera_id, customer=request.user)
            camera.delete()
            return Response({"status": True, "data": {"msg": "Successfully Deleted."}}, status=status.HTTP_403_FORBIDDEN)
        except Camera.DoesNotExist:
            try:
                camera_existence = Camera.objects.get(id = camera_id)
                return Response({"status": False, "data": {"msg": "You don't have permission to delete this camera."}}, status=status.HTTP_403_FORBIDDEN)
            except Camera.DoesNotExist:
                return Response({"status": False, "data": {"msg": "Camera not found."}}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status": False, "data": {"msg": str(e)}}, status=status.HTTP_400_BAD_REQUEST)
            
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
            try:
                header_existence = Header.objects.get(pk = header_id)
                return Response({"status": False, "data": {"msg": "You don't have permission to delete this data."}}, status=status.HTTP_403_FORBIDDEN)
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
        except Footer.DoesNotExist:
            try:
                footer_existence = Footer.objects.get(pk = footer_id)
                return Response({"status": False, "data": {"msg": "You don't have permission to delete this data."}}, status=status.HTTP_403_FORBIDDEN)
            except Footer.DoesNotExist:
                return Response({"status": False, "data": {"msg": "Footers not found."}}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status": False, "data": {"msg": str(e)}}, status=status.HTTP_400_BAD_REQUEST)
        
class CameraVoiceAPIView(APIView):
    
    permission_classes = [IsAdminOrCustomer]
    
    def get(self, request, *args, **kwargs):
        cameravoiceid = request.query_params.get('id')
        try:
            cameravoice = CameraVoice.objects.get(pk = cameravoiceid)
            serializer = CameraVoiceSerializer(cameravoice)
            camera_id = serializer.data.get('camera_id')
            cameradata = Camera.objects.get(pk = camera_id)
            customer_id = serializer.data.get('customer_id')
            customer = User.objects.get(pk = customer_id)
            data = {
                    "camera_voice_data": {
                        "id": serializer.data.get('id'), 
                        "customer_data": {
                            "id": customer.pk,
                            "username": customer.username          
                        },
                        "camera_data": {
                            "id": cameradata.pk,
                            "camera_seq_number": cameradata.camera_seq_number,
                            "camera_name" : cameradata.camera_name,
                            "camera_type" : cameradata.camera_type,
                        },
                        "wait_for_sec": serializer.data.get('wait_for_sec'),
                        "enter_or_exit_code": serializer.data.get('enter_or_exit_code'),
                        "text": serializer.data.get('text'),
                        "date": serializer.data.get('date')
                    }
                }
            print(data)
            return Response({"status": True, "data": data}, status=status.HTTP_200_OK)
        except CameraVoice.DoesNotExist:
            return Response({"status": False, "data": {"msg": "CameraVoice data doesn't exist."}})
    
    def post(self, request, *args, **kwargs):
        camera_id = request.data.get('camera_id')
        customer = request.user
        print(request.data.get('wait_for_sec'))
        try: 
            cameradata = Camera.objects.get(pk = camera_id)
            data = {
                'customer': customer.pk,
                'camera': cameradata.pk,
                'wait_for_sec': request.data.get('wait_for_sec'),
                'enter_or_exit_code': request.data.get('enter_or_exit_code'),
                'text': request.data.get('text')
            }
            serializer = CameraVoiceSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                data = {
                    "camera_voice_data": {
                            "id": serializer.data.get('id'), 
                            "customer_data": {
                                "id": customer.pk,
                                "username": customer.username          
                            },
                            "camera_data": {
                                "id": cameradata.pk,
                                "camera_seq_number": cameradata.camera_seq_number,
                                "camera_name" : cameradata.camera_name,
                                "camera_type" : cameradata.camera_type,
                            },
                            "wait_for_sec": serializer.data.get('wait_for_sec'),
                            "enter_or_exit_code": serializer.data.get('enter_or_exit_code'),
                            "text": serializer.data.get('text'),
                            "date": serializer.data.get('date')
                        }
                    }
                return Response({"status": True, "data": data})
            else:
                return Response({"status": False, "data": serializer.errors})
        except Camera.DoesNotExist:
            return Response({"status": False, "data": {"msg": "Camera doesn't exist."}}, status=status.HTTP_404_NOT_FOUND)
        
class CameraVoiceByCameraIdAPIView(APIView):
    
    permission_classes = [IsAdminOrCustomer]
    
    def get(self, request, *args, **kwargs):
        customer = request.user
        camera_id = request.query_params.get('camera_id')
        try:
            camera = Camera.objects.get(pk = camera_id)
            if customer.usertype == 1:
                CameraVoiceData = CameraVoice.objects.filter(camera = camera)
            elif customer.usertype == 2:    
                CameraVoiceData = CameraVoice.objects.filter(camera = camera, customer = customer)
            CameraVoice_Serializer = CameraVoiceSerializer(CameraVoiceData, many = True)
            response_data = CameraVoice_Serializer.data
            customized_response = []
            for item in response_data:
                customer = User.objects.get(pk = item['customer_id'])
                cameradata = Camera.objects.get(pk = item['camera_id'])
                data = {
                        "camera_voice_data": {
                            "id": item['id'], 
                            "customer_data": {
                                "id": customer.pk,
                                "username": customer.username          
                            },
                            "camera_data": {
                                "id": cameradata.pk,
                                "camera_seq_number": cameradata.camera_seq_number,
                                "camera_name" : cameradata.camera_name,
                                "camera_type" : cameradata.camera_type,
                            },
                            "wait_for_sec": item['wait_for_sec'],
                            "enter_or_exit_code": item['enter_or_exit_code'],
                            "text": item['text'],
                            "date": item['date']
                        }
                    }
                customized_response.append(data)
            return Response({"status": True, "data": customized_response})
        except Camera.DoesNotExist:
            return Response({"status": False, "data": {"msg": "Camera Doesn't Exist."}})
        
class GetAllCameraVoiceAPIView(APIView):
    
    permission_classes = [IsAdminOrCustomer]
    
    def get(self, request, *args, **kwargs):
        customer = request.user
        if customer.user_type == 2:
            CameraVoiceData = CameraVoice.objects.filter(customer = customer)
        elif customer.user_type == 1:
            CameraVoiceData = CameraVoice.objects.all()
        CameraVoice_Serializer = CameraVoiceSerializer(CameraVoiceData, many = True)
        response_data = CameraVoice_Serializer.data
        customized_response = []
        for item in response_data:
            customer = User.objects.get(pk = item['customer_id'])
            cameradata = Camera.objects.get(pk = item['camera_id'])
            data = {
                    "camera_voice_data": {
                        "id": item['id'], 
                        "customer_data": {
                            "id": customer.pk,
                            "username": customer.username          
                        },
                        "camera_data": {
                            "id": cameradata.pk,
                            "camera_seq_number": cameradata.camera_seq_number,
                            "camera_name" : cameradata.camera_name,
                            "camera_type" : cameradata.camera_type,
                        },
                        "wait_for_sec": item['wait_for_sec'],
                        "enter_or_exit_code": item['enter_or_exit_code'],
                        "text": item['text'],
                        "date": item['date']
                    }
                }
            customized_response.append(data)
        return Response({"status": True, "data": customized_response})
    
class DeleteCameraVoiceAPIView(APIView):
    permission_classes = [IsAdminOrCustomer]
    
    def post(self, request, *args, **kwargs):
        user = request.user
        id = request.data.get('id')
        if not id:
            return Response({"status": False, "data": {"msg": "CameraVoice ID is required."}}, status=status.HTTP_400_BAD_REQUEST)
        try:
            cameravoice = CameraVoice.objects.get(pk=id, customer = user)
        except CameraVoice.DoesNotExist:
            try:
                cameravoice_existence = CameraVoice.objects.get(pk=id)
                return Response({"status": False, "data": {"msg": "You don't have permission to delete this data."}}, status=status.HTTP_403_FORBIDDEN)
            except CameraVoice.DoesNotExist:
                return Response({"status": False, "data": {"msg": "CameraVoice Data Doesn't Exist"}}, status=status.HTTP_404_NOT_FOUND)
        
        cameravoice.delete()
        return Response({"status": True, "data": {"id": id}})
    
class UpdateCameraVoiceAPIView(APIView):
    
    permission_classes = [IsAdminOrCustomer]
    
    def post(self, request, *args, **kwargs):
        user = request.user
        id = request.data.get('id')
        user = request.user
        camera_id = request.data.get('camera_id')
        try:
            camera = Camera.objects.get(pk = camera_id)
        except Camera.DoesNotExist:
            return Response({"status": False, "data": {"msg": "Camera isn't Exist."}}, status=status.HTTP_404_NOT_FOUND)
        
        if not id:
            return Response({"status": False, "data": {"msg": "CameraVoice ID is required."}}, status=status.HTTP_400_BAD_REQUEST)
        try:
            cameravoice = CameraVoice.objects.get(pk=id, customer = user)
            data = {
                'customer': user.pk,
                'camera': camera.pk,
                'wait_for_sec': request.data.get('wait_for_sec'),
                'enter_or_exit_code': request.data.get('enter_or_exit_code'),
                'text': request.data.get('text')
            }
            serializer = CameraVoiceSerializer(cameravoice, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                updated_client = CameraVoice.objects.get(id=id)
                cameravoice_serializer = CameraVoiceSerializer(updated_client)
                data = {
                    "camera_voice_data": {
                            "id": id, 
                            "customer_data": {
                                "id": user.pk,
                                "username": user.username          
                            },
                            "camera_data": {
                                "id": camera.pk,
                                "camera_seq_number": camera.camera_seq_number,
                                "camera_name" : camera.camera_name,
                                "camera_type" : camera.camera_type,
                            },
                            "wait_for_sec": cameravoice_serializer.data.get('wait_for_sec'),
                            "enter_or_exit_code": cameravoice_serializer.data.get('enter_or_exit_code'),
                            "text": cameravoice_serializer.data.get('text'),
                            "date": cameravoice_serializer.data.get('date')
                        }
                    }
                return Response({'status': True, 'data': data})
        except CameraVoice.DoesNotExist:
            try:
                cameravoice_existence = CameraVoice.objects.get(pk=id)
                return Response({"status": False, "data": {"msg": "You don't have permission to update this data."}}, status=status.HTTP_403_FORBIDDEN)
            except CameraVoice.DoesNotExist:
                return Response({"status": False, "data": {"msg": "CameraVoice Data Doesn't Exist."}}, status=status.HTTP_404_NOT_FOUND)