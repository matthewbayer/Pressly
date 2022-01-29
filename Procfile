web: gunicorn newsletter.wsgi --log-file -
worker: python app/manage.py rqworker high default low