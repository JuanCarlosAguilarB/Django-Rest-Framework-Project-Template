#!/bin/sh

# apply database migrations
echo "---apply database migrations---"
/root/env/bin/python manage.py migrate --settings=core.settings.local

# runserver
echo "---run server---"
/root/env/bin/python manage.py runserver --settings=core.settings.local 0.0.0.0:8000
