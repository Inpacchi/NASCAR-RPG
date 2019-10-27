from flask import render_template
from flask_mail import Message

from webapp import app, mail


def send_email(subject, sender, recipients, text_body, html_body):
    message = Message(subject, sender=sender, recipients=recipients)
    message.body = text_body
    message.html = html_body

    mail.send(message)


def send_password_reset_email(user):
    token = user.get_reset_password_token()

    send_email('[NASRAC-NG] Reset Your Password',
               sender=app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/reset_password_body.txt', user=user, token=token),
               html_body=render_template('email/reset_password_body.html', user=user, token=token))
