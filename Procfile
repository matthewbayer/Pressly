web: gunicorn --log-file - --pythonpath="$PWD/app" config.wsgi:application
worker: python manage.py rqworker high default low