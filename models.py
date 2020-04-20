"""Models for Blogly."""
import datetime
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

def connect_db(app):
    """Connect to database"""

    db.app = app
    db.init_app(app)

class User(db.Model):
    """User. A User can have many posts"""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(25), nullable=False, unique=True)
    image_url = db.Column(db.Text, nullable=False, default="https://images.unsplash.com/photo-1533907650686-70576141c030")

    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")

    @property
    def full_name(self):
        """Return full name of user"""

        return f"{self.first_name} {self.last_name}"

class Post(db.Model):
    """Post"""

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(80), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    @property
    def friendly_date(self):
        """"Return user friendly date"""
        return f'{self.created_at.strftime("%b %d %Y %H:%M %p")}'
        

# SELECT id FROM users
# JOIN posts ON posts.user_id = users.id
