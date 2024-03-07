"""
WSGI config for rtback project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
from dotenv import load_dotenv


from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rtback.settings')

ENVFILE = os.getenv('DJANGO_ENV', 'development')
env_file = f".env.{ENVFILE}"
load_dotenv(dotenv_path=env_file)


application = get_wsgi_application()

