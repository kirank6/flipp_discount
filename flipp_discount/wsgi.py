"""
WSGI config for flipp_discount project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os
from subprocess import call
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flipp_discount.settings')

application = get_wsgi_application()


# def application(env, start_response):
#     body = b'Thank you!\n' # for python3 it should be bytes
#     status = '200 OK'
#     headers = [('Content-Type', 'text/html')]
#     start_response(status,headers)
#     return [body]