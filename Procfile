release: python manage.py migrate --noinput
web: gunicorn work_at_codevance.wsgi --log-file -
beat: celery -A work_at_codevance beat