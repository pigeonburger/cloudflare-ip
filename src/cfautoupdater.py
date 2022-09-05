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

# Get the server's public IP
def get_public_ip():
	# Get the public IP of the server
	current_ip_json = requests.get(PUBLIC_IP_API_URL)
	# Status code should be 200, otherwise the API is probably down
	if current_ip_json.status_code != 200:
		print(f"[WARN] {now()} - Can't get current IP. Retrying...")
		time.sleep(10)
		current_ip_json = get_public_ip()
	return current_ip_json

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
	finally:
		print(f"[INFO] {now()} - Email sent.")


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
 
	# Looping forever
	while True:
		current_ip = get_public_ip().json()['ip']
		print(f"[INFO] {now()} - Current public IP is: {current_ip}")
		# Get all the A records or just the one selected
		if RECORD_ID:
			records = requests.get(CLOUDFLARE_URL + "?type=A", headers=header).json()
		else:
			records = requests.get(CLOUDFLARE_URL + f"/{RECORD_ID}", headers=header).json()
		records_names = ""
		for record in records['result']:
			print(f"[INFO] {now()} - Record \"{record['name']}\" IP: {record['content']}")
			# Change the IP using a PATCH request if the current IP is different from the one in the record
			if record['content'] != current_ip:
				payload = {"content": current_ip}
				requests.patch(CLOUDFLARE_URL + f"/{record['id']}", headers=header, data=json.dumps(payload))
				print(f"[INFO] {now()} - Record \"{record['name']}\" IP change from {record['content']} to {current_ip}")
				records_names += record['name'] + ', '
		# Send email
		if SENDER_ADDRESS & SENDER_PASSWORD & RECEIVER_ADDRESS:
			print(f"[INFO] {now()} - Sending email...")
			send_email(current_ip, records['result'][0]['content'], records_names[:-1])
		# Wait before next check
		print(f"[INFO] {now()} - Wait {CHECK_INTERVAL} seconds before next check", end="\n-----")
		time.sleep(CHECK_INTERVAL)

if __name__ == '__main__':
	main()