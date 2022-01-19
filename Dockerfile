FROM python:3.7-alpine3.15

RUN pip3 install requests

ENV ZONE_ID="" \
    EMAIL="" \
    AUTH_KEY="" \
    RECORD_ID="none" \
    CHECK_INTERVAL=86400

RUN wget https://raw.githubusercontent.com/Daru-0/cloudflare-ip/main/cfautoupdater.py; chmod +x /cfautoupdater.py

RUN wget https://raw.githubusercontent.com/Daru-0/cloudflare-ip/main/entrypoint.sh; chmod +x /entrypoint.sh

ENTRYPOINT /entrypoint.sh