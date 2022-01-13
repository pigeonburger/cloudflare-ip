# Cloudflare DNS Auto IP Updater


This is a fork of the script [pigeonburger/cloudflare-ip](https://github.com/pigeonburger/cloudflare-ip). I added a Dockerfile to run the script inside an alpine container, which is very lightweight.

The entrypoint will check if the environment variables have been correctly inputted

The script will check the public IP every 24 hours and automatically update an A record's IP address if they are different. Of course the container with the script must be in the same network as the record you want to change.

Be aware, this only works if your site is on the Cloudflare CDN. See the requirements below:

<h2>Requirements:</h2>

  - A Cloudflare account
  - Cloudflare API Bearer Token (at least with DNS Edit permissions)
  - Zone ID
  - The ID of the A record ([how to](https://api.cloudflare.com/#dns-records-for-a-zone-list-dns-records))
  
</br>

<h2>Installation:</h2>


    docker run -d \
      -e BEARER_TOKEN=<YOUR_BEARER_TOKEN> \
      -e RECORD_ID=<YOUR_DNS_RECORD_ID> \
      -e ZONE_ID=<YOUR_ZONE_ID> \
      daruzero/cfautoupdater:latest

</br>

## Future implementation
- Add possibility to choose the amount of time between public IP's checks
- Add possibility to change more than one A record
- Re-add possibility to log changes via mail
- Add volume to store log in the local filesystem
- Check ENV validity in entrypoint.sh
- Refine code