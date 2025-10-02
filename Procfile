web: gunicorn portfolio_blog.wsgi:application --bind 0.0.0.0:$PORT
release: python manage.py migrate --settings=portfolio_blog.settings_railway