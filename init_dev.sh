py.test -x
touch temp.db && rm temp.db
django-admin.py syncdb --noinput
django-admin.py migrate --all --noinput
django-admin.py demo_data_login
django-admin.py demo_data_crm
django-admin.py demo_data_invoice

django-admin.py runserver
