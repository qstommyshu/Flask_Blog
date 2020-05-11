import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flask_app import mail


def save_picture(form_picture):
    #use hex to encrypt secret token
    random_hex = secrets.token_hex(8)
    #split the path of the file and the file extension (the file might be represented in the whole path name)
    _, f_ext = os.path.splitext(form_picture.filename)
    #total file name is equal to the random hex plus the extension???
    #once the user uploaded their file, the system need to store it
    #with the name of hex token so that it doesn't duplicate, keep the same type of file so same extension
    picture_fn = random_hex + f_ext
    #set a path to store the picture
    picture_path = os.path.join(current_app.root_path, 'static/image', picture_fn)
    #control the size of the picture
    output_size = (125, 125)
    #open the image and store it as an image object
    i = Image.open(form_picture)
    #resize the picture object as the output size
    i.thumbnail(output_size)
    #save the object to specific path
    i.save(picture_path)
    #does it have to be here??
    #yes, in account function return this picture so that it is easier for that to work
    return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    print(user.email)
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)