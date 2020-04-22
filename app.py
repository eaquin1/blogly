"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = "shhhh"

debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
db.create_all()

@app.route("/")
def redirect_userlist():
    """List of all posts"""
    posts = Post.query.all()
    return render_template("postlist.html", posts=posts)

@app.route("/users")
def render_userlist():
    """Render userlist"""
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template("userlist.html", users=users)

@app.route("/users/new", methods=["GET"])
def render_newuser_form():
    """Form for a new user"""
    return render_template('users/new.html')

@app.route("/users/new", methods=["POST"])
def submit_form():
    """Submit form data to database"""
    first_name = request.form['first-name']
    last_name = request.form['last-name']
    image_url = request.form['img-url']
    if image_url == '':
        image_url = None

    user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(user)
    db.session.commit()

    flash(f"User {user.full_name} added")

    return redirect('/users')

@app.route("/users/<int:user_id>")
def show_user(user_id):
    """Show individual user"""
    user = User.query.get_or_404(user_id)

    return render_template("users/detail.html", user=user)
    
@app.route("/users/<int:user_id>/edit")
def render_edit_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("users/edit.html", user=user)

@app.route("/users/<int:user_id>/edit", methods=["POST"])
def edit_user(user_id):
    """Handle form submission for updating an existing user"""
    user = User.query.get_or_404(user_id)

    user.first_name = request.form['first-name']
    user.last_name = request.form['last-name']
    user.image_url = request.form['img-url']

    db.session.add(user)
    db.session.commit()
    flash(f"User {user.full_name} edited")

    return redirect("/users")

@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """Delete user from database"""
    user = User.query.filter_by(id = user_id).first()
    db.session.delete(user)
    db.session.commit()
    flash(f"User {user.full_name} deleted")
    return redirect("/users")

@app.route("/users/<int:user_id>/posts/new")
def add_post(user_id):
    """Form for user to add new post"""
    user = User.query.get_or_404(user_id)
    return render_template("posts/new.html", user=user)

@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def handle_post(user_id):
    """Handle form submission for a new post"""
    user = User.query.get_or_404(user_id)
    title = request.form['title']
    content = request.form['content']

    post = Post(user=user, title=title, content=content)
    db.session.add(post)
    db.session.commit()
    flash(f"Post '{post.title}' added")

    return redirect(f'/users/{user.id}')    

# ************POST ROUTES***************

@app.route("/posts/<int:post_id>")
def show_post(post_id):
    """Show details of a single post"""
    post = Post.query.get_or_404(post_id)
    tags = post.tags
    return render_template('posts/detail.html', post=post, tags=tags)

@app.route("/posts/<int:post_id>/edit")
def edit_post(post_id):
    """Render edit post form"""
    post = Post.query.get_or_404(post_id)
    tags = post.tags

    return render_template('posts/edit.html', post=post, tags=tags)

@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def handle_edit(post_id):
    """"Handle edit post"""
    post = Post.query.get_or_404(post_id)

    post.title = request.form['title']
    post.content = request.form['content']
    post.tags.name = request.form.getlist('tags[]')
    print(f"POSTS ARE BLUE {post.tags.name}")

    db.session.add(post)
    db.session.commit()

    return redirect(f'/posts/{post.id}')

@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    """Delete post"""
    post = Post.query.filter_by(id = post_id).first()
    db.session.delete(post)

    db.session.commit()

    flash(f"Post '{post.title}' deleted")
    return redirect("/")

@app.errorhandler(404)
def page_not_found(e):
    """Custom 404 page"""
    return render_template("404.html"), 404

# ***********Tag routes**********

@app.route("/tags")
def list_tags():
    """List all tags"""
    tags = Tag.query.all()

    return render_template("tags/list.html", tags=tags)

@app.route("/tags/<int:tag_id>")
def show_tag_detail(tag_id):
    """Show all posts associated with tag"""
    tag = Tag.query.get(tag_id)
    posts = tag.posts

    return render_template("tags/detail.html", tag=tag, posts=posts)


@app.route("/tags/new")
def render_new_tag_form():
    """Show form for new tag"""

    return render_template("tags/new.html")

@app.route("/tags/new", methods=["POST"])
def handle_new_tag():
    """Handle submission of new tag"""
    name = request.form["name"]

    new_tag = Tag(name=name)
    db.session.add(new_tag)
    db.session.commit()
    return redirect('/tags')

@app.route("/tags/<int:tag_id>/edit")
def render_edit_tag(tag_id):
    """Show form to edit tag"""
    tag = Tag.query.get(tag_id)
    return render_template("tags/edit.html", tag=tag)

@app.route("/tags/<int:tag_id>/edit", methods=["POST"])
def handle_edit_tag(tag_id):
    """Handle Edit tag submission"""
    edit_tag = Tag.query.get(tag_id)

    edit_tag.name = request.form["name"]
    db.session.add(edit_tag)
    db.session.commit()
  
    return redirect('/tags')

@app.route("/tags/<int:tag_id>/delete", methods=["POST"])
def delete_tag(tag_id):
    delete_tag = Tag.query.filter_by(id = tag_id).first()
    
    db.session.delete(delete_tag)
    db.session.commit()
    
    return redirect('/tags')


