"""Models for Cupcake app."""
# from typing import Sized
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMG_URL = "https://tinyurl.com/demo-cupcake"


def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)


class Cupcake(db.Model):
    """Cupcake"""

    __tablename__ = "cupcakes"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True)

    flavor = db.Column(
        db.Text,
        nullable=False)

    size = db.Column(
        db.Text,
        nullable=False)

    rating = db.Column(
        db.Integer,
        nullable=False)

    image = db.Column(
        db.String,
        nullable=False,
        default=DEFAULT_IMG_URL)

    def serialize(self):
        """Serialize to dictionary."""

        return {
            "id": self.id,
            "flavor": self.flavor,
            "size": self.size,
            "rating": self.rating,
            "image": self.image
        }
