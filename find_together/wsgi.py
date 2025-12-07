"""
WSGI config for find_together project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'find_together.settings')

application = get_wsgi_application()
