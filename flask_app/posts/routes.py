from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flask_app import db
from flask_app.models import Post
from flask_app.posts.forms import PostForm

posts = Blueprint('posts', __name__)


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        #include all the attributes of a post when creating a post
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post', form=form, lengend='New Post')


@posts.route("/post/<int:post_id>")
def post(post_id):
    #(Post.query.get) is a method to get post object from database by id
    #in this case is either get or just return a 404 
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    #current user cannot update the post if he is not the author
    if post.author != current_user:
        abort(403)
    form = PostForm()
    #if the author is not current user, it atomatically goes to the previous if loop
    #didn't mention here so it assume authoer is the current user
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', post=post, form=form, lengend='Upadate Post')


#the triangle is an variable of post_id
@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    #get the post from database
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    #delete the post from database
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))
