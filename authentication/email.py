import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_mail(sender_email,sender_name, sender_password, recipient_email, subject, body):
    message = MIMEMultipart()
    message["From"] = f"{sender_name}"
    message["To"] = recipient_email
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))
    
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            text = message.as_string()
            server.sendmail(sender_email, recipient_email, text)
        print("Email delivered successfully")
    except Exception as e:
        print(f"An error occurred: {e}")

def send_email(subject, message, recipient_email):
    sender_email = "kwakuasihene@gmail.com"
    sender_name = "Dreamosoft"
    sender_password = "gfkwisqhckdtqmoq"
    send_mail(sender_email,sender_name, sender_password, recipient_email, subject, message)