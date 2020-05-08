import os
import secrets
from PIL import Image
from flask_app.models import User, Post
from flask_app import app, db, bcrypt, mail
from flask import render_template, url_for, flash, redirect, request, abort
from flask_app.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                             PostForm, RequestResetForm, ResetPasswordForm)
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message




#Create a list contains dictionary store information and be able to loop through
# posts = [
#     {
#         'author':'Tommy',
#         'title':'Blog Post 1',
#         'content':'First post content',
#         'date_posted':'April 27,2020'
#     },
#     {
#         'author':'Jango',
#         'title':'Blog Post 2',
#         'content':'Second post content',
#         'date_posted':'April 27,2020'
#     }
# ]





















