from django.core.wsgi import get_wsgi_application
import os
import sys

# Add project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_blog.settings_vercel')

# Initialize Django
application = get_wsgi_application()

# Vercel needs this exact function name
def handler(event, context):
    return application(event, context)