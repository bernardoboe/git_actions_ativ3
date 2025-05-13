FROM python:3.10-slim

WORKDIR /app
COPY . /app

RUN pip install flask flask-restx gunicorn

EXPOSE 80

CMD ["gunicorn", "-b", "0.0.0.0:80", "conecta_postgres:app"]
