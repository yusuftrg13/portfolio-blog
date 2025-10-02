#!/bin/bash

# Build script for Vercel
echo "Creating staticfiles directory..."
python3.9 -m pip install -r requirements.txt
python3.9 manage.py collectstatic --noinput --clear