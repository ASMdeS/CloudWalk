import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def write_email(body):
    # Email details
    sender_email = "monitoringanalysttest@outlook.com"
    receiver_email = "arthursmds@gmail.com"
    subject = "Anomaly detected"

    # SMTP server details
    smtp_server = "smtp-mail.outlook.com"
    smtp_port = 587
    password = "rmebVRT25NRLgmH"

    # Create the email
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Send the email
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Secure the connection
        server.login(sender_email, password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email. Error: {e}")
    finally:
        server.quit()
