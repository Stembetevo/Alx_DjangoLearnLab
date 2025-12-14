"""
WSGI Configuration for PythonAnywhere

Copy this content to your WSGI configuration file in PythonAnywhere.
Path: /var/www/yourusername_pythonanywhere_com_wsgi.py
"""

import os
import sys
from dotenv import load_dotenv

# ============================================================================
# 🔧 CONFIGURATION 
# ============================================================================
PYTHONANYWHERE_USERNAME = os.getenv('USERNAME')
# ============================================================================

# Add your project directory to the sys.path
project_home = f'/home/{PYTHONANYWHERE_USERNAME}/Alx_DjangoLearnLab/social_media_api'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Load environment variables from .env file
env_path = os.path.join(project_home, '.env')
load_dotenv(env_path)

# Set the Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'social_media_api.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_media_api.settings')

# Import Django's WSGI handler
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
