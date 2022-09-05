from smtplib import SMTPAuthenticationError, SMTPConnectError, SMTPRecipientsRefused, SMTPSenderRefused
import requests, time, json, datetime, os, yagmail

PUBLIC_IP_API_URL = "https://api.ipify.org?format=json"
ZONE_ID = os.getenv('ZONE_ID')
CLOUDFLARE_URL = f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records"
SENDER_PASSWORD = os.getenv('SENDER_PASSWORD')
SENDER_ADDRESS = os.getenv('SENDER_ADDRESS')
RECEIVER_ADDRESS = os.getenv('RECEIVER_ADDRESS')

# Get the current time
def now():
	return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Handle any API errors
def handling_api_errors(current_ip_json, ipcheck_status):
	while ipcheck_status != 200:
		print(f"[WARN] {now()} - Can't get current IP. Retrying...")
		time.sleep(10)
		current_ip_json = requests.get(PUBLIC_IP_API_URL)
		ipcheck_status = current_ip_json.status_code

	return current_ip_json, ipcheck_status

# Get the server's public IP
def get_public_ip():
	# Get the public IP of the server
	current_ip_json = requests.get(PUBLIC_IP_API_URL)
	# Status code should be 200, otherwise the API is probably down
	ipcheck_status = current_ip_json.status_code
	current_ip_json, ipcheck_status = handling_api_errors(current_ip_json, ipcheck_status)
	current_ip = current_ip_json.json()['ip']

	return current_ip

# Send email
def send_email(current_ip, record_ip, record_name):
	try:
		with yagmail.SMTP(SENDER_ADDRESS, SENDER_PASSWORD) as server:
			server.send(
				to=RECEIVER_ADDRESS,
				subject="Public IP change",
				contents=f"The public IP of the record(s) {record_name} has changed from {record_ip} to {current_ip}."
			)
	except SMTPSenderRefused:
		print(f"[ERROR] {now()} - Can't send email. The sender address is invalid.")
	except SMTPAuthenticationError:
		print(f"[ERROR] {now()} - Can't send email. Check your credentials.")
	except SMTPRecipientsRefused:
		print(f"[ERROR] {now()} - Can't send email. Check your receiver address.")
	except SMTPConnectError:
		print(f"[ERROR] {now()} - Can't send email. Check your internet connection.")


def main():
	# Getting environment variables
	EMAIL =  os.getenv('EMAIL')
	AUTH_KEY = os.getenv('AUTH_KEY')
	RECORD_ID = os.getenv('RECORD_ID')
	CHECK_INTERVAL = int(os.getenv('CHECK_INTERVAL'))
	# Setting the header for the requests to the CloudFlare API
	header = {
  		"X-Auth-Email": EMAIL, 
		"X-Auth-Key": AUTH_KEY,
  		"content-type": "application/json"
		}
 
 # Handle multiple records
	if RECORD_ID == "none":
		while True:
			# Get the current IP
			current_ip = get_public_ip()
			print(f"[INFO] {now()} - Current public IP is: {current_ip}")
			# Get all the A records
			records = requests.get(CLOUDFLARE_URL + "?type=A", headers=header).json()
			records_names = ''
			for record in records['result']:
				print(f"[INFO] {now()} - Record \"{record['name']}\" IP: {record['content']}")
				if record['content'] != current_ip:
					# Payload to serve the CloudFlare API
					payload = {"content": current_ip}
					# Change the IP using a PATCH request
					requests.patch(CLOUDFLARE_URL + f"/{record['id']}", headers=header, data=json.dumps(payload))
					# Log change
					print(f"[INFO] {now()} - Record \"{record['name']}\" IP change from {record['content']} to {current_ip}")
					record_name += record['name'] + ', '
			# Send email
			if SENDER_ADDRESS & SENDER_PASSWORD & RECEIVER_ADDRESS:
				send_email(current_ip, record_ip, records_names)

			# Wait before next check
			print(f"[INFO] {now()} - Wait {CHECK_INTERVAL} seconds before next check", end="\n-----")
			time.sleep(CHECK_INTERVAL)
	# Handle single record
	else:
		while True:
			# Get the data of the A Record
			record = requests.get(CLOUDFLARE_URL + f"/{RECORD_ID}", headers=header).json()
			record_ip = record['result']['content']
			record_name = record['result']['name']
			# Get the current IP
			current_ip = get_public_ip()
			# Log info
			print(f"[INFO] {now()} - Current public IP is: {current_ip}")
			print(f"[INFO] {now()} - Record \"{record_name}\" IP: {record_ip}")

			# This loop checks your live IP every 24 hours to make sure that it's the same one as set in your DNS record
			while current_ip == record_ip:
					time.sleep(CHECK_INTERVAL) # Default wait 86400s (24h)
					current_ip = get_public_ip()

			# Payload to serve the CloudFlare API
			payload = {"content": current_ip}

			# Change the IP using a PATCH request
			requests.patch(CLOUDFLARE_URL + f"/{RECORD_ID}", headers=header, data=json.dumps(payload))
			
			# Log change
			print(f"[INFO] {now()} - IP change from {record_ip} to {current_ip}")

			# Send email
			if SENDER_ADDRESS & SENDER_PASSWORD & RECEIVER_ADDRESS:
				send_email(current_ip, record_ip, record_name)

if __name__ == '__main__':
	main()