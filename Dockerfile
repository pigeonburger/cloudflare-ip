FROM python:3.6-alpine3.15

RUN apk add --update apk-cron && rm -rf /var/cache/apk/*

RUN pip install requests

ADD ./cfauth.ini /

ADD https://raw.githubusercontent.com/Daru-0/cloudflare-ip/main/cfautoupdater.py /

ADD https://raw.githubusercontent.com/Daru-0/cloudflare-ip/main/entry.sh /

RUN chmod +x /cfautoupdater.py /entry.sh

RUN cfautoupdater.py

CMD ["/entry.sh"]