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

    def __init__(self, email, username, first_name, last_name, password):
        """Init function"""
        self.email = email
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.secure_password = self.hash_password(password)

    @property
    def password(self):
        raise AttributeError("You cannot read password attribute")

    @password.setter
    def password(self, password):
        self.secure_password = generate_password_hash(password)

    @staticmethod
    def hash_password(password1):
        """Hashes user password"""
        return generate_password_hash(password1)

    @staticmethod
    def verify_password(saved_password, password1):
        """Check is password hash matches actual password"""
        return check_password_hash(saved_password, password1)

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


@dataclass
class Book(db.Model):
    """Book Model"""
    # Ensure table name is in plural
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), index=True)
    author = db.Column(db.String(100), index=True)
    isbn = db.Column(db.String(100), index=True, unique=True)
    publisher = db.Column(db.String(100), index=True)
    quantity = db.Column(db.Integer)
    availability = False
    created = db.Column(db.Date, default=datetime.today())
    reviewers = db.relationship(
        'User', secondary='reviewed_books', lazy='dynamic')

    def __init__(self, title, author, isbn, publisher, quantity):
        """Init function"""
        self.title = title
        self.author = author
        self.isbn = isbn
        self.publisher = publisher
        self.quantity = quantity
    @staticmethod
    def get_all_books():
        """Gets all book"""
        return Book.query.all()

    @staticmethod
    def get_book_by_id(id):
        """Gets book by id"""
        return Book.query.filter_by(id=id).first()

    @staticmethod
    def search(q):
        books = Book.query.filter(
            or_(Book.title.like('%' + q.title() + '%'))).all()
        return {"Books": [book.serialize for book in books]}

    @property
    def serialize(self):
        """Serializes book information"""
        self.availability = self.quantity != 0
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "publisher": self.publisher,
            "availability": self.availability,
            "quantity": self.quantity
        }

    def save(self):
        """Saves book object to database"""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Deletes book object"""
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "Book: {}".format(self.title)


class ReviewBook(db.Model):
    """Association Table"""
    __tablename__ = "reviewed_books"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))
    date_reviewed = db.Column(db.Date, default=datetime.today())
    date_of_review = db.Column(db.Date, default=datetime.today() + timedelta(days=30), nullable=True)
    reviewed = db.Column(db.Boolean, default=False)
    user = db.relationship(User, backref='book')
    book = db.relationship(Book, backref='user')

    @staticmethod
    def get_all_reviewed_books():
        """Gets all books in review table"""
        return ReviewBook.query.all()

    @staticmethod
    def get_user_review_history(user_id):
        """ Gets user review history"""
        reviewed_books = ReviewBook.get_all_reviewed_books()
        user_books = [
            book for book in reviewed_books if book.user_id == user_id]
        review_history = []
        book_details = {}
        for book in user_books:
            try:
                single_book = Book.get_book_by_id(book.book_id)
                book_details["id"] = single_book.id
                book_details["title"] = single_book.title
                book_details["author"] = single_book.author
                book_details["isbn"] = single_book.isbn
                book_details["review_date"] = book.date_reviewed
                if book.reviewed:
                    book_details["reviewed_date"] = book.date_reviewed
                else:
                    book_details["review_date"] = book.date_of_review
            except Exception as e:
                print(e)
            finally:
                review_history.append(book_details)
                book_details = {}
        return review_history

    @staticmethod
    def get_books_not_reviewed(user_id):
        """Gets books not reviewed by user"""
        reviewed_books = ReviewBook.get_all_reviewed_books()
        # User non reviewed books
        user_books = [book for book in reviewed_books if book.user_id ==
                      user_id and book.returned == False]
        unreviewed_books = []
        book_details = {}
        for book in user_books:
            try:
                single_book = Book.get_book_by_id(book.book_id)
                book_details["id"] = single_book.id
                book_details["title"] = single_book.title
                book_details["author"] = single_book.author
                book_details["isbn"] = single_book.isbn
                book_details["reviewDate"] = book.date_reviewed
                book_details["dueDate"] = book.date_due
            except Exception as e:
                print(f'error {e}')
            finally:
                unreviewed_books.append(book_details)
                book_details = {}
        return unreviewed_books

    def save(self):
        """Saved book reviewed to database"""
        db.session.add(self)
        db.session.commit()


@dataclass
class Token(db.Model):
    """Token Model"""
    __tablename__ = 'tokens'

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(1000), index=True, unique=True)
    owner = db.Column(db.String(60))
    created = db.Column(db.DateTime, default=datetime.today())

    def __init__(self, token, owner):
        """Init function"""
        self.token = token
        self.owner = owner


    @staticmethod
    def all_tokens():
        """Gets all tokens"""
        return Token.query.all()

    @staticmethod
    def token_by_owner(username):
        """Gets token by user's username"""
        return Token.query.filter_by(owner=username).first()

    def save(self):
        """Saves generated token to database."""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Delete token after being revoked"""
        db.session.delete(self)
        db.session.commit()


@dataclass
class Revoked(db.Model):
    """Revoked Token Table"""

    __tablename__ = 'revoked'
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(1000), index=True)
    date_revoked = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, token):
        """Init function"""
        self.token = token

    @staticmethod
    def is_blacklisted(token):
        """Checks if token is revoked"""
        return bool(Revoked.query.filter_by(token=token).first())

    def save(self):
        """Saves revoked token to database"""
        db.session.add(self)
        db.session.commit()
