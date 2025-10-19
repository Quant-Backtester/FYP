#STL
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

#Custom
from core import settings

def send_email(to_email: str, subject: str, body: str) -> None:
    # For development: just print to console
    if settings.debug:
        print(f"\n EMAIL TO: {to_email}")
        print(f"SUBJECT: {subject}")
        print(f"BODY:\n{body}\n")
        return

    # Production: use real SMTP (need an actual email)
    msg = MIMEMultipart()
    msg["From"] = settings.smtp_user
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP_SSL(settings.smtp_host, settings.smtp_port) as server:
        server.login(settings.smtp_user, settings.smtp_password)
        server.send_message(msg)