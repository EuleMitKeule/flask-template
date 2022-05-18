FROM python:3.10-slim

COPY . /app
COPY ./scripts/entrypoint.sh /entrypoint.sh

WORKDIR /app

RUN apt-get clean \
    && apt-get -y update \
    && apt-get -y install nginx \
    && apt-get -y install python3-dev \
    && apt-get -y install build-essential \
    && pip install --upgrade pip \
    && pip install -r requirements.txt

COPY ./config/nginx.conf /etc/nginx/nginx.conf

RUN chown -R www-data:www-data /app \
    && chmod +x /entrypoint.sh

CMD ["/entrypoint.sh"]
