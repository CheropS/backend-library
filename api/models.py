from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from dataclasses import dataclass
from api import db
from sqlalchemy import or_


@dataclass
class User(db.Model):
    """User Model"""
    # Ensure table name is in plural
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    secure_password = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    joined = db.Column(db.Date, default=datetime.today())
    reviewed_books = db.relationship(
        'Book', secondary='reviewed_books', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError("You cannot read password attribute")

    @password.setter
    def password(self, password):
        self.secure_password = generate_password_hash(password)

    @staticmethod
    def hash_password(password):
        """Hashes user password"""
        return generate_password_hash(password)

    @staticmethod
    def verify_password(saved_password, password):
        """Check is password hash matches actual password"""
        return check_password_hash(saved_password, password)

    def save(self):
        """Saves user objects to database"""
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def all_users():
        """Gets all users"""
        return User.query.all()

    @staticmethod
    def get_user_by_username(username):
        """Gets user by username"""
        return User.query.filter_by(username=username).first()

    def update_password(self, password):
        """Updates user's password"""
        self.secure_password = User.hash_password(password)
        User.save(self)

    @property
    def serialize(self):
        """Serializes User object"""
        return {
            "email": self.email,
            "username": self.username,
            "firstName": self.first_name,
            "lastName": self.last_name,
            "is_admin": self.is_admin,
        }

    @property
    def promote(self):
        """Promotes normal user to admin"""
        self.is_admin = True
        User.save(self)
        return f'User: {self.username} is now an admin'

    @staticmethod
    def promote_user(username):
        """Promotes normal user to admin in tests"""
        user = User.get_user_by_username(username)
        user.is_admin = True
        user.save()

    def admin(self):
        """Checks if user is an admin"""
        return bool(self.is_admin)

    def __repr__(self):
        return "User: {}".format(self.username)

