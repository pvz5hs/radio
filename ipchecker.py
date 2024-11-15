import socket
import smtplib
from email.mime.text import MIMEText
import os

# Function to get the private IP
def get_private_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        private_ip = s.getsockname()[0]
        s.close()
        return private_ip
    except Exception as e:
        return None

# Function to send an email
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

# Function to monitor and handle IP changes
def monitor_ip_change():
    # Path to store the previous IP
    ip_file = "last_ip.txt"

    # Get the current private IP
    current_ip = get_private_ip()
    if not current_ip:
        print("Unable to retrieve IP address.")
        return

    # Check if there's a stored IP
    if os.path.exists(ip_file):
        with open(ip_file, 'r') as file:
            last_ip = file.read().strip()
    else:
        last_ip = None

    # Compare and act if IP has changed
    if current_ip != last_ip:
        print(f"IP has changed: {last_ip} -> {current_ip}")
        # Update the stored IP
        with open(ip_file, 'w') as file:
            file.write(current_ip)

        # Email credentials and recipient
        sender_email = "astrobradrequests@gmail.com"

        # export EMAIL_PASSWORD="ksno dlby fhvs vhzm"
        sender_password = os.getenv("EMAIL_PASSWORD")
        print(sender_password)
        if not sender_password:
            raise ValueError("EMAIL_PASSWORD environment variable is not set.")

        recipient_email = "pvz5hs@virginia.edu"

        # Send email notification
        subject = "Private IP Address Changed"
        body = f"Your private IP address has changed from {last_ip or 'N/A'} to {current_ip}."
        send_email(subject, body, sender_email, sender_password, recipient_email)
    else:
        print("IP has not changed.")

if __name__ == "__main__":
    monitor_ip_change()
