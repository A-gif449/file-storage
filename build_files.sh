#!/bin/bash

# Install Python dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Create a dummy dist directory for Vercel
mkdir -p dist
echo "Vercel build complete" > dist/index.html