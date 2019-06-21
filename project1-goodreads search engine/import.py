import csv
import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# database engine object from SQLAlchemy that manages connections to the database
engine = create_engine(os.getenv("DATABASE_URL"))

db = scoped_session(sessionmaker(bind=engine))



class Book(db.model):
    __tablename__='book'
    isbn = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.string)
    author = db.Column(db.string)
    year = db.Column(db.integer)

    def __init__(self,isbn,title,author,year):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.year = year

def main():
    with open('books.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            entry = Book({row["isbn"]},{row["title"]},{row["author"]},{row["year"]})
            db.session.add(entry)
            print(f"added {row['title']} into database")
        db.commit()

if __name__ == '__main__':
    db.create_all()
    main()



