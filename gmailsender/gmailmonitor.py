import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

def send_email(subject, body, to_email, video_path):
    sender_email = "otis1880town@gmail.com"
    sender_password = "JackBox729@"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = subject

    # Attach the body with MIMEText
    msg.attach(MIMEText(body, 'plain'))

    if os.path.isfile(video_path):
        attachment = MIMEBase('application', 'octet-stream')
        with open(video_path, 'rb') as video_file:
            attachment.set_payload(video_file.read())
        encoders.encode_base64(attachment)
        attachment.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(video_path)}"')
        msg.attach(attachment)
    else:
        print(f"Error: File {video_path} does not exist")

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(sender_email, sender_password)
    server.send_message(msg)
    server.quit()
    print("Email sent successfully!")

# Example usage
send_email("Tour Video for you", "This is a tour video for you.", "codemaster9428@gmail.com", "D:\Project\MyProject\OttisTourist\\1880_video_backend\\1880_video_backend\staticfiles/media\\videos\\1717812656077_3b40556b4280abb2.mp4")

# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText

# def send_email(subject, body, to_email):
#     sender_email = "otis1880town@gmail.com"
#     sender_password = "JackBox729@"

#     # Create MIMEMultipart message
#     msg = MIMEMultipart()
#     msg['From'] = sender_email
#     msg['To'] = to_email
#     msg['Subject'] = subject

#     # Attach the body with MIMEText
#     msg.attach(MIMEText(body, 'plain'))

#     # Create server object with SSL option
#     server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    
#     # Login to the server
#     server.login(sender_email, sender_password)

#     # Send the email
#     server.send_message(msg)
    
#     # Quit the server
#     server.quit()

#     print("Email sent successfully!")