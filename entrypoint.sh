python manage.py collectstatic --noinput

#python manage.py makemigrations

python manage.py migrate

# gunicorn Moshaver.wsgi:application --bind 0.0.0.0:8000
python manage.py runserver 0.0.0.0:8000
#tail -f /dev/null
