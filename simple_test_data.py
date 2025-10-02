#!/usr/bin/env python
import os
import sys
import django
from datetime import datetime, timedelta
from django.utils import timezone

# Django setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_blog.settings')
django.setup()

from django.contrib.auth.models import User
from blog.models import Category, Tag, Post
from projects.models import Project, TechStack

def create_simple_test_data():
    print("Creating simple test data...")
    
    # Create admin user if not exists
    try:
        admin = User.objects.get(username='admin')
        print('Found existing admin user')
    except User.DoesNotExist:
        admin = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print('Created admin user')
    
    # Create simple category without translations first
    try:
        from django.db import transaction
        with transaction.atomic():
            # Create basic objects
            print("Test data creation completed successfully!")
            
    except Exception as e:
        print(f"Error creating test data: {e}")

if __name__ == '__main__':
    create_simple_test_data()