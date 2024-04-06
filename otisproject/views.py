from django.http import HttpResponse
from django.conf import settings
import os

def serve_react_app(request):
    with open(os.path.join(settings.BASE_DIR, 'templates', 'index.html'), 'r') as file:
        return HttpResponse(file.read())
