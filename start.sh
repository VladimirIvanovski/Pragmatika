#!/bin/bash
# Production start script

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Install dependencies if needed
if [ ! -d "venv" ] || [ "$1" == "--install" ]; then
    pip install -r requirements.txt
fi

# Create necessary directories
mkdir -p documents static/extracted_images content

# Run with gunicorn for production
if command -v gunicorn &> /dev/null; then
    gunicorn --bind 0.0.0.0:${PORT:-5000} \
             --workers ${WORKERS:-4} \
             --timeout 120 \
             --access-logfile - \
             --error-logfile - \
             app:app
else
    # Fallback to Flask development server
    python app.py
fi
