import socket
import smtplib
from email.mime.text import MIMEText
import os

def get_private_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        private_ip = s.getsockname()[0]
        s.close()
        return private_ip
    except Exception as e:
        return None

def send_email(subject, body, sender_email, sender_password, recipient_email):
    try:
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = recipient_email

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

def monitor_ip_change():
    ip_file = "last_ip.txt"

    current_ip = get_private_ip()
    if not current_ip:
        print("Unable to retrieve IP address.")
        return

    if os.path.exists(ip_file):
        with open(ip_file, 'r') as file:
            last_ip = file.read().strip()
    else:
        last_ip = None

    # Compare and act
    if current_ip != last_ip:
        print(f"IP has changed: {last_ip} -> {current_ip}")
        # updte
        with open(ip_file, 'w') as file:
            file.write(current_ip)

        # email creds
        sender_email = "astrobradrequests@gmail.com"

        # export EMAIL_PASSWORD="password" in terminal, ill email you the password
        sender_password = os.getenv("EMAIL_PASSWORD")
        print(sender_password)
        if not sender_password:
            raise ValueError("EMAIL_PASSWORD environment variable is not set.")
	#Change to your email
        recipient_email = "pvz5hs@virginia.edu"

        # Send email notification
        subject = "Private IP Address Changed"
        body = f"Your private IP address has changed from {last_ip or 'N/A'} to {current_ip}."
        send_email(subject, body, sender_email, sender_password, recipient_email)
    else:
        print("IP has not changed.")

if __name__ == "__main__":
    monitor_ip_change()
