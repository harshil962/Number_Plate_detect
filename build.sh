#!/usr/bin/env bash
set -e

pip install torch==2.1.0+cpu torchvision==0.16.0+cpu --extra-index-url https://download.pytorch.org/whl/cpu
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate