#!/usr/bin/env bash
# Build script for Render

set -o errexit  # exit on error

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input --settings=portfolio_blog.settings_production

# Run database migrations
python manage.py migrate --settings=portfolio_blog.settings_production