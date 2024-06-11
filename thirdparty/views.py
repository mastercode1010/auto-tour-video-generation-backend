from rest_framework.views import APIView
from rest_framework.response import Response
import requests
import json
from rest_framework import status

class CameraCheckAPIView(APIView):
    def post(self, request):
        userdata = request.data
        print(userdata)
        ip_addr = userdata["camera_ip"]
        userName = userdata["userName"]
        password = userdata["password"]

        url = f'https://{ip_addr}/api.cgi?cmd=Login'
        headers = {
            'Content-Type': 'application/json'
        }
        data = [
            {
                "cmd": "Login",
                "param": {
                    "User": {
                        "Version": "0",
                        "userName": userName,
                        "password": password
                    }
                }
            }
        ]
        try:
            response = requests.get(url, headers=headers, data=json.dumps(data), verify=False)
            response.raise_for_status()
            
            # Parse the JSON response
            data = json.loads(response.text)
            print(data)
            print(data[0]["code"])
            return Response({"status": True, "data": "Connected"}, status=status.HTTP_200_OK)
        
        except requests.exceptions.HTTPError as http_err:
            return Response({"status": False, "data": f'HTTP error occurred: {http_err}', 'content': response.content.decode()}, status=status.HTTP_400_BAD_REQUEST)
        except requests.exceptions.ConnectionError as conn_err:
            return Response({"status": False, "data": f'Connection error occurred: {conn_err}'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except requests.exceptions.Timeout as timeout_err:
            return Response({"status": False, "data": f'Timeout error occurred: {timeout_err}'}, status=status.HTTP_504_GATEWAY_TIMEOUT)
        except requests.exceptions.RequestException as req_err:
            return Response({"status": False, "data": f'Request error occurred: {req_err}'}, status=status.HTTP_400_BAD_REQUEST)
        except json.JSONDecodeError as json_err:
            return Response({"status": False, "data": f'JSON decode error: {json_err}', 'content': response.text}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response({"status": False, "data": str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
