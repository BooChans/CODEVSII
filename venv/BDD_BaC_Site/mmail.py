from flask_mail import Message

from .tools.extensions import mail
from BDD_BaC_Site import app

def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=app.config["MAIL_DEFAULT_SENDER"],
    )
    mail.send(msg)