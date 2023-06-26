#!/bin/sh

# apply database migrations
echo "---apply database migrations---"
/root/env/bin/python manage.py migrate --settings=core.settings.local

# create superuser by default
echo "---create superuser---"
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python manage.py shell --settings=core.settings.local

# runserver
echo "---run server---"
/root/env/bin/python manage.py runserver --settings=core.settings.local 0.0.0.0:8000
