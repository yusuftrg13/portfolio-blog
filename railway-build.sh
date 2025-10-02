#!/bin/bash

# Railway build script
echo "Starting Railway build..."

# Install dependencies
pip install -r requirements.txt

# Set Django settings
export DJANGO_SETTINGS_MODULE=portfolio_blog.settings_railway

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate

echo "Build completed successfully!"