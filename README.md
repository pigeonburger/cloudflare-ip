# Cloudflare DNS Auto IP Updater

This is a script I made that will automatically update my A record's IP address whenever my web server's IP changes.

I don't have (nor can I afford) a static ip, meaning that my IP address constantly changes. Whenever it <i>does</i> change (usually while I'm sleeping), it means that my site becomes completely inaccessible. So, I attempted to create a solution, which is this script. It can also send you an email and log all IP changes to a file to let you know it's been updated.

Be aware, this only works if your site is on the Cloudflare CDN. See the requirements below:

<h2>Requirements:</h2>

  - Python 3.6 or above
  - Python requests library (install using `pip3 install requests`)
  - A Cloudflare account with website
  - Cloudflare API Bearer Token
  - Need to know your zone ID
  - The ID of the A record you want to change
  
  
<h2>Optional:</h2>

  - SMTP email, to send an update when the IP changes
  
 
<h2>Installation:</h2>

On your web server, in any directory, clone this repository:

    git clone https://github.com/pygeonburger/cloudflare-ip/
        
Then, open the file `cfauth.ini` in that folder and replace `<YOUR_ZONE_ID>` with your actual Cloudflare Zone ID, `<YOUR_BEARER_TOKEN>` with your API bearer token and `<YOUR_DNS_RECORD_ID>` with the ID of the DNS record you want to change.

Then, if you've done everything, run the `cfautoupdater.py` file!