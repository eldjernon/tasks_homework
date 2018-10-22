import smtplib
from tasks.exceptions import EmailSendError

host = ""
port = 587
username = "username"
password = "password"
from_email = ""
to_email = ""

server = smtplib.SMTP(host=host, port=port)
server.login(user=username, password=password)


def send_email(msg):
    try:
        server.sendmail(from_addr=from_email, to_addrs="", msg=msg)
    except smtplib.SMTPException as exc:
        raise EmailSendError(f"Email send error: {exc}")
