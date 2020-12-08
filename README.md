# Cloudflare DNS Auto IP Address Updater

This is a script I made that will automatically update my A record's IP address whenever my web server's IP changes.

I don't have (nor can I afford) a static ip, meaning that my IP address constantly changes. Whenever it <i>does</i> change (usually while I'm sleeping), it means that my site becomes completely inaccessible. So, I attempted to create a solution, which is this script. It can also send you an email to let you know it's been updated.

Be aware, this only works if your site is on Cloudflare, AND you have direct access to the web server (root permissions are not required). See the requirements below:

<h2>Requirements:</h2>

  - Python 3.6 or above
  - Python requests library (install using `pip3 install requests`)
  - A Cloudflare account
  - Cloudflare API Bearer Token
  - Access to your server's file system
  - Need to know your zone ID
  - You'll also need to know the ID of the A record you want to change
  
  
<h2>Optional:</h2>

  - SMTP email, to send an update when the IP changes
  
 
<h2>Installation:</h2>

On your web server, in any directory, clone this repository:

    git clone https://github.com/pygeonburger/cf-auto-ip-updater/
        
Then, create a file called `cfauth.ini` in that cloned folder and set it up like so:

    [tokens]
    zone_id=<YOUR_ZONE_ID>
    bearer_token=<YOUR_BEARER_TOKEN>
    record_id=<YOUR_DNS_RECORD_ID>
        
Replacing `<YOUR_ZONE_ID>` with your actual Cloudflare Zone ID, `<YOUR_BEARER_TOKEN>` with your API bearer token and `<YOUR_DNS_RECORD_ID>` with the ID of the DNS record you want to change.

Then, if you've done everything, run the `cfautoupdater.py` file!

To keep this script running forever, rather than just stopping once it changes your DNS record's ID, I just use the <a href="https://github.com/immortal/immortal">Immortal</a> package.
