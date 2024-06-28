from threading import Thread
from flask_mail import Message
from flask import render_template, current_app
from . import mail

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()

def send_reset_password_email(user, new_password):
    send_email('[YourApp] Reset Your Password',
               sender=current_app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/new_password.txt', user=user, new_password=new_password),
               html_body=render_template('email/new_password.html', user=user, new_password=new_password))

def send_reservation_confirmation_email(user, reservation, ticket_code):
    send_email('[YourApp] Reservation Confirmation',
               sender=current_app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/reservation_confirmation.txt', user=user, reservation=reservation, ticket_code=ticket_code),
               html_body=render_template('email/reservation_confirmation.html', user=user, reservation=reservation, ticket_code=ticket_code))

def send_cancellation_email(user, reservation):
    send_email('[YourApp] Reservation Cancellation',
               sender=current_app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/cancellation_email.txt', user=user, reservation=reservation),
               html_body=render_template('email/cancellation_email.html', user=user, reservation=reservation))

