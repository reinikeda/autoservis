# syntax=docker/dockerfile:1
FROM python:slim-buster
WORKDIR /app
COPY ./autoservis .
COPY ./requirements.txt .
RUN pip install -r requirements.txt
# RUN python manage.py collectstatic --noinput
# RUN python manage.py migrate
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
# CMD ["gunicorn", "-b", "0.0.0.0:8000", "autoservis.wsgi"]