from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from werkzeug.security import check_password_hash
from sqlalchemy.orm import relationship

app = Flask(__name__)
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.CHAR)
    password = db.Column(db.String, nullable =False)
    user_reviews = relationship("Review")

    def __init__(self, username,password):
        self.username = username
        self.password = password

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String)
    date_posted = db.Column(db.String)
    rating = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('books.id')) #relationship is to the tablename, not class

    def __init__(self, id,  content, date_posted, rating, user_id, book_id):
        self.id = id
        self.content = content
        self.date_posted = date_posted
        self.user_id = user_id
        self.rating = rating
        self.book_id = book_id

class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String)
    title = db.Column(db.String)
    author = db.Column(db.String)
    publication_date = db.Column(db.Integer)
    book_reviews = relationship("Review")

    def __init__(self, id,  isbn, title, author, publication_date):
        self.id = id
        self.isbn = isbn
        self.title = title
        self.author = author
        self.publication_date = publication_date