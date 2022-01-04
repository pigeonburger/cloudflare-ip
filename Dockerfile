FROM python:3.6-alpine3.15

ENV APP_PATH=/usr/src/app

WORKDIR ${APP_PATH}

RUN pip3 install requests

ENV ZONE_ID=""
ENV BEARER_TOKEN=""
ENV RECORD_ID=""

ADD https://raw.githubusercontent.com/Daru-0/cloudflare-ip/main/cfautoupdater.py ./cfautoupdater.py

ADD https://raw.githubusercontent.com/Daru-0/cloudflare-ip/main/entrypoint.sh ./entrypoint.sh

ENTRYPOINT ${APP_PATH}/entrypoint.sh