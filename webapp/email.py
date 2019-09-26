from flask import render_template
from flask_mail import Message

from webapp import app, mail

def sendEmail(subject, sender, recipients, textBody, htmlBody):
    message = Message(subject, sender=sender, recipients=recipients)
    message.body = textBody
    message.html = htmlBody

    mail.send(message)

def sendPasswordResetEmail(user):
    token = user.getResetPasswordToken()

    sendEmail('[NASRAC-NG] Reset Your Password',
              sender=app.config['ADMINS'][0],
              recipients=[user.email],
              textBody=render_template('email/resetPasswordBody.txt', user=user, token=token),
              htmlBody=render_template('email/resetPasswordBody.html', user=user, token=token))
