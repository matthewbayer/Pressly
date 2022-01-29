web: gunicorn newsletter.wsgi --log-file - --pythonpath="$PWD/app"
worker: python manage.py rqworker high default low