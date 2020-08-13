import secrets
import os
from buynow import app, mail
from PIL import Image
from buynow.models import Customer
from flask_mail import Message
from flask import url_for

def save_picture(form_picture, folder, size_x, size_y):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    image_fn = random_hex + f_ext
    image_path = os.path.join(app.root_path, 'static/'+folder, image_fn)

    output_size = (size_x, size_y)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(image_path)

    return image_fn

def delete_old_picture(image_filename, folder):
    image_path = os.path.join(app.root_path, 'static/'+folder, image_filename)
    os.remove(image_path)

def send_reset_email(customer):
    token = customer.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=[customer.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset.reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)