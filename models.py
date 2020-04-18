"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    """Connect to database"""

    db.app = app
    db.init_app(app)

class User(db.Model):
    """User"""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(25), nullable=False, unique=True)
    image_url = db.Column(db.String, default="https://images.unsplash.com/photo-1533907650686-70576141c030")