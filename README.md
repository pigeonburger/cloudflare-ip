# Cloudflare DNS Auto IP Updater


This is a fork of the script [pigeonburger/cloudflare-ip](https://github.com/pigeonburger/cloudflare-ip). I added a Dockerfile to run the script inside an alpine container, which is very lightweight.

The entrypoint will check if the environment variables have been correctly inputted.

The script will check the public IP every 24 hours and automatically update one (or all) of the A records' IP address if they are different.

Be aware, this only works if your content is on the Cloudflare CDN.

## Requirements:

  - A CloudFlare account
  - Cloudflare Global API Key
  - ID of the Zone you want to change a record of
  - (optional) The ID of the A record you want to change ([how to](https://api.cloudflare.com/#dns-records-for-a-zone-list-dns-records))
  
</br>

## Installation:

```
docker run -d \
  -e EMAIL=<YOUR_CF_LOGIN_EMAIL> \
  -e AUTH_KEY=<YOUR_API_KEY> \
  -e ZONE_ID=<YOUR_ZONE_ID> \
  daruzero/cfautoupdater:latest
```
### Enviroment variables:

(required) `ZONE_ID`: The ID of the zone you want to change a record of  
(required) `EMAIL`: Email used for the CloudFlare registration  
(required) `AUTH_KEY`: Your CloudFlare Global API Key  
(optional) `RECORD_ID`: The ID of the record you want to change. Insert "none" to update all the A record of the zone (this is the default if not set)  
(optional) `CHECK_INTERVAL`: The amount of seconds the script should wait between checks (default 86400)  

</br>

## Future implementation
- [x] Add possibility to choose the amount of time between public IP's checks
- [x] Add possibility to change more than one A record
- [x] Check ENV validity in entrypoint.sh
- [ ] Add possibility to log changes via mail
- [ ] Easy standalone script that can run without a container