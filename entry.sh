#!/bin/sh

# Echo the cronjob into the crontab
echo "@daily /cfautoupdater.py >> /script.log" >> /usr/bin/crontab

# Start cron
/usr/sbin/crond -f -l 8