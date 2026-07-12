import os

from flask_mail import Message

from placementportalcode.extensions import mail


def send_email(subject,recipients,body,attachment_path=None, attachment_name=None,content_type="text/csv",html=None):
   
    msg = Message(
        subject=subject,
        recipients=recipients
    )

    msg.body = body
    if html:
        msg.html = html
    if attachment_path:

        if attachment_name is None:
            attachment_name = os.path.basename(attachment_path)

        with open(attachment_path, "rb") as file:
            msg.attach(
                filename=attachment_name,
                content_type=content_type,
                data=file.read()
            )

    mail.send(msg)