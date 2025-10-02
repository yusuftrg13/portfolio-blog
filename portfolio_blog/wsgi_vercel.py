import os
import sys
from django.core.wsgi import get_wsgi_application

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_blog.settings_vercel')

application = get_wsgi_application()

# Vercel handler
def handler(request):
    return application(request.environ, request.start_response)