import logging
import smtplib
from email.mime.multipart import MIMEMultipart

from app import settings
from app.exceptions.send_email import SendEmailException


class SmtpService:
    def __init__(self, host, port, email, password):
        self._smtp_server = host
        self._smtp_port = port
        self._email = email
        self._password = password

    def send(self, message: MIMEMultipart) -> None:
        try:
            with smtplib.SMTP(self._smtp_server, self._smtp_port) as server:
                server.starttls()
                server.login(self._email, self._password)
                server.sendmail(self._email, message['To'], message.as_string())
                server.quit()
        except Exception as e:
            logging.error(e)
            raise SendEmailException(e)


def get_smtp_service() -> SmtpService:
    return SmtpService(
        host='smtp.gmail.com', port=587, email=settings.CORPARATION_EMAIL, password=settings.CORPARATION_EMAIL_PASSWORD
    )
