import os
import secrets
from PIL import Image
from flask_app.models import User, Post
from flask_app import app, db, bcrypt
from flask import render_template, url_for, flash, redirect, request, abort
from flask_app.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from flask_login import login_user, current_user, logout_user, login_required




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


@app.route("/")
@app.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html',title = 'about')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data, email = form.email.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()
        #pass a one time message to front end, category is success
        flash('Your account have now been created, you are now able to login', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    #if all the fields are filled and submitted
    if form.validate_on_submit():
        #search for the user in database
        user = User.query.filter_by(email=form.email.data).first()
        #if the the decrypt password is same as the form submitted password,login;else not
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            #If there is a next page request, redirect to next page
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:   
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout", methods=['GET', 'POST'])
def logout():
    #logout user
    logout_user()
    return redirect(url_for('home'))


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
    picture_path = os.path.join(app.root_path, 'static/image', picture_fn)
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



@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        #if the user updated the picture
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        #just simple update
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    #if user just access this page but didn't change anything
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    #get the path and name of image file
    image_file = url_for('static', filename='image/' + current_user.image_file)
    #render template but pass title, image_file and form so that all these can be properly display on the page
    return render_template('account.html', title='Account', image_file=image_file, form=form)


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post', form=form, lengend='New Post')


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', post=post, form=form, lengend='Upadate Post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))


@app.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username = username).first_or_404()
    posts = Post.query.filter_by(author = user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)