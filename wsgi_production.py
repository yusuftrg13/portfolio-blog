#!/usr/bin/env python
"""WSGI config for production deployment."""

import os
from django.core.wsgi import get_wsgi_application

# Set production settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_blog.settings_production')

application = get_wsgi_application()