#!/bin/bash

# Ensure folders exist
mkdir -p images/input images/output images/archive

# Set environment variables
export FLASK_APP=app.py
export FLASK_ENV=production

# Start with Gunicorn for production
exec gunicorn --bind 0.0.0.0:5000 --workers 2 --timeout 120 --keep-alive 2 --max-requests 1000 --max-requests-jitter 100 app:app
