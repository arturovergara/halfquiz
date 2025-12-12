#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

python3 /app/halfquiz/manage.py collectstatic --no-input
python3 /app/halfquiz/manage.py migrate --no-input

# Start production server
gunicorn --bind 0.0.0.0:8000 --workers=4 config.wsgi:application
