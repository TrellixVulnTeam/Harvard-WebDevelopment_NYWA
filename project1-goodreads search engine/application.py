# -*- coding: utf-8 -*- 

import os
from model import *

from flask import Flask, session, redirect, render_template, request, jsonify, flash
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, or_
from sqlalchemy.orm import scoped_session, sessionmaker

from werkzeug.security import generate_password_hash, check_password_hash
from helpers import login_required



# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# database engine object from SQLAlchemy that manages connections to the database
engine = create_engine(os.getenv("DATABASE_URL"))

# create a 'scoped session' that ensures different users' interactions with the
# database are kept separate
with app.app_context():
	db.create_all()

@app.route("/")
@login_required
def index():
	return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])#The login route validates the login variables on login.
def login():

	session.clear()

	if request.method == 'POST':

		# checking if there is such an account:
		pw = request.form.get("password")
		name = request.form.get('username')
		user = User.query.filter_by(username=name).first()


		if user and check_password_hash(user.password,pw):
			session['logged_in'] = True
			session['username'] = user
			return redirect("/")


		else:
			return render_template("error.html", message="Invalid username and/or password")



	# User reached route via GET (as by clicking a link or via redirect)

	return render_template('login.html')


@app.route("/logout")
def logout():
	session['logged_in'] = False
	return redirect("/login")

@app.route("/register",methods=["GET","POST"])
def register():

	if request.method == 'POST':
		user_id = request.form.get("username")

		#check if the username exist,render error message otherwise
		user_check = User.query.filter_by(username=user_id).first()
		if user_check:
			render_template("error.html",message="username already exist")

		#creating hashed password_id
		password = request.form.get("password")
		password_id = generate_password_hash(password)
		new_user = User(username=user_id,password=password_id)
		db.session.add(new_user)
		db.session.commit()
		
		# Redirect user to login page
		return redirect("/login")

	return render_template('register.html')

@app.route("/search", methods=["GET"])
@login_required
def search():
	if not request.args.get("book"):
		return render_template("error.html", message="you must provide a book.")

	# Take input and add a wildcard
	search_query = ("%" + request.args.get("book") + "%").title()
	# Capitalize all words of input for search with a wildcard
	# https://docs.python.org/3.7/library/stdtypes.html?highlight=title#str.title
	results = Book.query.filter_by(or_((Book.isbn.like(search_query)) , (Book.author.like(search_query)) , (Book.title.like(search_query)))).all()

	if results ==0 or None:
		render_template("error.html",message="Sorry we are unable to find that book you requested.")

	render_template("result.html",results = results)


@app.route("/book/<isbn>", methods=['GET', 'POST'])
@login_required
def book(isbn):
	""" Save user review and load same page with reviews updated."""

	if request.method == "POST":

		# Save current user info
		currentUser = session["username"]

		# Fetch form data
		rating = request.form.get("rating")
		comment = request.form.get("comment")

		# Search book_id by ISBN
		row = db.execute("SELECT id FROM books WHERE isbn = :isbn",
						 {"isbn": isbn})

		# Save id into variable
		bookId = row.fetchone()  # (id,)
		bookId = bookId[0]

		# Check for user submission (ONLY 1 review/user allowed per book)
		row2 = db.execute("SELECT * FROM reviews WHERE user_id = :user_id AND book_id = :book_id",
						  {"user_id": currentUser,
						   "book_id": bookId})

		# A review already exists
		if row2.rowcount == 1:
			flash('You already submitted a review for this book', 'warning')
			return redirect("/book/" + isbn)

		# Convert to save into DB
		rating = int(rating)

		db.execute("INSERT INTO reviews (user_id, book_id, comment, rating) VALUES \
                    (:user_id, :book_id, :comment, :rating)",
				   {"user_id": currentUser,
					"book_id": bookId,
					"comment": comment,
					"rating": rating})

		# Commit transactions to DB and close the connection
		db.commit()

		flash('Review submitted!', 'info')

		return redirect("/book/" + isbn)

	# Take the book ISBN and redirect to his page (GET)
	else:

		row = db.execute("SELECT isbn, title, author, year FROM books WHERE \
                        isbn = :isbn",
						 {"isbn": isbn})

		bookInfo = row.fetchall()

		""" GOODREADS reviews """

		# Read API key from env variable
		key = os.getenv("GOODREADS_KEY")

		# Query the api with key and ISBN as parameters
		query = request.get("https://www.goodreads.com/book/review_counts.json",
							 params={"key": key, "isbns": isbn})

		# Convert the response to JSON
		response = query.json()

		# "Clean" the JSON before passing it to the bookInfo list
		response = response['books'][0]

		# Append it as the second element on the list. [1]
		bookInfo.append(response)

		""" Users reviews """

		# Search book_id by ISBN
		row = db.execute("SELECT id FROM books WHERE isbn = :isbn",
						 {"isbn": isbn})

		# Save id into variable
		book = row.fetchone()  # (id,)
		book = book[0]

		# Fetch book reviews
		# Date formatting (https://www.postgresql.org/docs/9.1/functions-formatting.html)
		results = db.execute("SELECT users.username, comment, rating, \
                            to_char(time, 'DD Mon YY - HH24:MI:SS') as time \
                            FROM users \
                            INNER JOIN reviews \
                            ON users.id = reviews.user_id \
                            WHERE book_id = :book \
                            ORDER BY time",
							 {"book": book})

		reviews = results.fetchall()

		return render_template("book.html", bookInfo=bookInfo, reviews=reviews)


@app.route("/api/<isbn>", methods=['GET'])
@login_required
def api_call(isbn):
	# COUNT returns rowcount
	# SUM returns sum selected cells' values
	# INNER JOIN associates books with reviews tables

	row = db.execute("SELECT title, author, year, isbn, \
                    COUNT(reviews.id) as review_count, \
                    AVG(reviews.rating) as average_score \
                    FROM books \
                    INNER JOIN reviews \
                    ON books.id = reviews.book_id \
                    WHERE isbn = :isbn \
                    GROUP BY title, author, year, isbn",
					 {"isbn": isbn})

	# Error checking
	if row.rowcount != 1:
		return jsonify({"Error": "Invalid book ISBN"}), 422

	# Fetch result from RowProxy
	tmp = row.fetchone()

	# Convert to dict
	result = dict(tmp.items())

	# Round Avg Score to 2 decimal. This returns a string which does not meet the requirement.
	# https://floating-point-gui.de/languages/python/
	result['average_score'] = float('%.2f' % (result['average_score']))

	return jsonify(result)
