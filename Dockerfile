FROM python:3.7-alpine3.15

COPY src/ /app

WORKDIR /app

RUN pip3 install requests yagmail

ENV ZONE_ID="" \
    EMAIL="" \
    AUTH_KEY="" \
    RECORD_ID="" \
    CHECK_INTERVAL=86400 \
    SENDER_ADDRESS="" \
    SENDER_PASSWORD="" \
    RECEIVER_ADDRESS=""

ENTRYPOINT ["/bin/sh", "/app/entrypoint.sh"]
