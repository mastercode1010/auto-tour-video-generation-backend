"""
WSGI config for otisproject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

import sys

import site

from django.core.wsgi import get_wsgi_application

sys.path.append('D:/Project/MyProject/OttisTourist')
sys.path.append('D:/Project/MyProject/OttisTourist/otisproject')

os.environ['DJANGO_SETTINGS_MODULE'] = 'otisproject.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'otisproject.settings')

application = get_wsgi_application()

