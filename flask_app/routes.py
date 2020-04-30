from flask_app.models import User, Post
from flask_app import app
from flask import render_template, url_for, flash, redirect
from flask_app.forms import RegistrationForm, LoginForm




#Create a list contains dictionary store information and be able to loop through
posts = [
    {
        'author':'Tommy',
        'title':'Blog Post 1',
        'content':'First post content',
        'date_posted':'April 27,2020'
    },
    {
        'author':'Jango',
        'title':'Blog Post 2',
        'content':'Second post content',
        'date_posted':'April 27,2020'
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html',posts=posts)


@app.route("/about")
def about():
    return render_template('about.html',title = 'about')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        #pass a one time message to front end, category is success
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)