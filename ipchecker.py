import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import socket
import requests
import os



# File to store the last known IP address
IP_FILE = "last_known_ip.txt"

def get_public_ip():
    """Retrieve the current public IP address."""
    try:
        response = requests.get("https://api.ipify.org?format=text", timeout=5)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching public IP: {e}")
        return None

def send_email(new_ip):
    """Send an email notifying the recipient of the new IP address."""
    sender_email = "astrobradrequests@gmail.com"
    sender_password = os.getenv("EMAIL_PASSWORD")

    # export EMAIL_PASSWORD="your_app_password"
    if not sender_password:
        raise ValueError("EMAIL_PASSWORD environment variable is not set.")


    recipient_email = "recipient@example.com"  # Replace with the recipient email

    subject = "IP Address Change Notification"
    body = f"The new IP address is: {new_ip}"

    # Create the email message
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        # Connect to the SMTP server and send the email
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
        print(f"Email sent successfully to {recipient_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")

def check_ip_change():
    """Check if the IP address has changed and take action if it has."""
    current_ip = get_public_ip()
    if not current_ip:
        return

    # Read the last known IP from the file
    if os.path.exists(IP_FILE):
        with open(IP_FILE, "r") as file:
            last_ip = file.read().strip()
    else:
        last_ip = None

    # If the IP has changed, update the file and send an email
    if current_ip != last_ip:
        with open(IP_FILE, "w") as file:
            file.write(current_ip)
        print(f"IP address changed to {current_ip}")
        send_email(current_ip)
    else:
        print("IP address has not changed.")

if __name__ == "__main__":
    check_ip_change()
