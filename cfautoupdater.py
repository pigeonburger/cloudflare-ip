import requests, time, json, configparser, smtplib

# Reading the keys from the cfauth.ini file
config = configparser.ConfigParser()
config.read('cfauth.ini')

zone_id = config.get('tokens', 'zone_id')
bearer_token = config.get('tokens', 'bearer_token')
record_id = config.get('tokens', 'record_id')

# The headers we want to use
headers = {
    "Authorization": f"Bearer {bearer_token}", 
    "content-type": "application/json"
    }

while True:
    # Getting the initial data of your A Record
    a_record_url = requests.get(f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}", headers=headers)
    arecordjson = a_record_url.json()

    # This is the current IP that your chosen A record has been set to on Cloudflare
    current_set_ip = arecordjson['result']['content']

    # This gets your current live external IP (whether that is the same as the A record or not)
    currentip = requests.get("https://api.ipify.org?format=json")

    # Status code should be 200, otherwise the API is probably down (this can happen quite a bit)
    ipcheck_status = currentip.status_code

    # Handling any API errors (otherwise we'd be trying to change the IP to some random HTML)
    while ipcheck_status != 200:
        time.sleep(10)
        currentip = requests.get("https://api.ipify.org?format=json")
        ipcheck_status = currentip.status_code

    currentactualip = currentip.json()['ip']

    # This loop checks your live IP every 5 minutes to make sure that it's the same one as set in your DNS record
    while currentactualip == current_set_ip:
        time.sleep(300) # Wait for 300 seconds (5 minutes)
        currentip = requests.get("https://api.ipify.org?format=json") # Then it checks if your IP is still the same or not.
        ipcheck_status = currentip.status_code

    # Handling any API errors AGAIN
        while ipcheck_status != 200:
            time.sleep(10)
            currentip = requests.get("https://api.ipify.org?format=json")
            ipcheck_status = currentip.status_code

        currentactualip = currentip.json()['ip']

    else: # If your live IP is NOT the same as the A Record's IP
        pass

    # The "Payload" is what we want to change in the DNS record JSON (in this case, it's our IP)
    payload = {"content": currentactualip}

    # Change the IP using a PATCH request
    requests.patch(f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}", headers=headers, data=json.dumps(payload))


    # Sends an email to you to let you know everything has been updated.
    # If you don't want this, just delete everything below this comment.

    sender = 'sender@google.com'
    receivers = ['receiver@example.com']

    message = f"""From: Server <sender@google.com>
    To: Your email <receiver@example.com>
    Subject: DNS IP Updated

    The server's IP has changed from {current_set_ip} to {currentactualip}.

    The DNS records have been updated.
    """

    smtpObj = smtplib.SMTP('smtp.example.com', port=587)
    smtpObj.connect("smtp.example.com", port=587)
    smtpObj.ehlo()
    smtpObj.starttls()
    smtpObj.login("username", "password")
    smtpObj.sendmail(sender, receivers, message)