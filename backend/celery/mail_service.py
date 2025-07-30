import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from backend.models import User

SMTP_SERVER = "localhost"
SMTP_PORT = 1025
SENDER_EMAIL = 'admin@parkeasy'
SENDER_PASSWORD = ''

def send_email(to, subject, content):
    message = MIMEMultipart()
    message['To'] = to
    message['Subject'] = subject
    message['From'] = SENDER_EMAIL
    
    message.attach(MIMEText(content, 'html'))

    with smtplib.SMTP(host=SMTP_SERVER, port=SMTP_PORT) as client:
        client.send_message(message)
        client.quit()

# send_email('namitguptadelhi@gmail.com', 'Test2 Email', '<h1>Welcome to Vehicle Parking</h1>')
