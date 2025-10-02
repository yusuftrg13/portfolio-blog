#!/bin/bash

# Build script for Vercel
echo "Creating staticfiles directory..."
pip install -r requirements.txt
python manage.py collectstatic --noinput --clear