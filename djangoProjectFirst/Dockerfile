FROM ubuntu:latest
LABEL authors="aplyg"


WORKDIR /firstblog

COPY . /firstblog

# Устанавливаем Python и pip
RUN apt-get update && apt-get install -y python3-pip

# Устанавливаем зависимости проекта
RUN pip install -r requirements.txt

CMD python manage.py runserver 0.0.0.0:8000
