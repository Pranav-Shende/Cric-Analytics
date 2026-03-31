#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --noinput

python manage.py migrate
#python manage.py loaddata cricket_data.json
# python manage.py load_cricket_data_batting
# python manage.py load_cricket_data_bowling
# python manage.py load_cricket_data_fielding

