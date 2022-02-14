FROM python:3.8


RUN set -xe \
    && apt-get update \
    && apt-get install -y python3-pip



ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY . /app

EXPOSE 8000

CMD python app.py

