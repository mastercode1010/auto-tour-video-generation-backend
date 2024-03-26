import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(subject, body, to_email):
    sender_email = "otis1880town@gmail.com"
    sender_password = "JackBox729@"

    # Create MIMEMultipart message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = subject

    # Attach the body with MIMEText
    msg.attach(MIMEText(body, 'plain'))

    # Create server object with SSL option
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    
    # Login to the server
    server.login(sender_email, sender_password)

    # Send the email
    server.send_message(msg)
    
    # Quit the server
    server.quit()

    print("Email sent successfully!")

