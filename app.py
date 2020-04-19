"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

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
    """Redirect to users"""
    return redirect('/users')

@app.route("/users")
def render_userlist():
    """Render userlist"""
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template("userlist.html", users=users)

@app.route("/users/new", methods=["GET"])
def render_newuser_form():
    """Form for a new user"""
    return render_template('new.html')

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

    return redirect('/users')

@app.route("/users/<int:user_id>")
def show_user(user_id):
    """Show individual user"""
    user = User.query.get_or_404(user_id)
    return render_template("detail.html", user=user)
    
@app.route("/users/<int:user_id>/edit")
def render_edit_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("edit.html", user=user)

@app.route("/users/<int:user_id>/edit", methods=["POST"])
def edit_user(user_id):
    """Handle form submission for updating an existing user"""
    user = User.query.get_or_404(user_id)

    user.first_name = request.form['first-name']
    user.last_name = request.form['last-name']
    user.image_url = request.form['img-url']

    db.session.add(user)
    db.session.commit()

    return redirect("/users")

@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """Delete user from database"""
    user = User.query.filter_by(id = user_id).delete()
    db.session.commit()

    return redirect("/users")

    
