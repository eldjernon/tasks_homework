from typing import Text

import smtplib
import os

from tasks.exceptions import EmailSendError

HOST = os.getenv("EMAIL_HOST", "")
PORT = int(os.getenv("EMAIL_PORT", 587))
USERNAME = os.getenv("EMAIL_USERNAME", "")
PASSWORD = os.getenv("EMAIL_PASSWORD", "")
FROM_ADDR = os.getenv("EMAIL_FROM_ADDR", "")


class EmailSender:
    """
    Simple email sender, to using is need set env variables:
    EMAIL_HOST
    EMAIL_PORT: default 587
    EMAIL_USERNAME
    EMAIL_PASSWORD
    EMAIL_FROM_ADDR
    """

    def __init__(self):
        try:
            server = smtplib.SMTP(host=HOST, port=PORT)
            server.connect()
            server.ehlo()
            server.starttls()
            server.login(user=USERNAME, password=PASSWORD)
            self.server = server
        except (smtplib.SMTPException, ConnectionRefusedError) as exc:
            raise EmailSendError(f"Email server configuration error: {exc}.")

    def send_email(self, msg: Text, to_addr: Text):
        try:
            self.server.sendmail(from_addr=FROM_ADDR, to_addrs=to_addr, msg=msg)
        except smtplib.SMTPException as exc:
            raise EmailSendError(f"Email send error: {exc}.")
