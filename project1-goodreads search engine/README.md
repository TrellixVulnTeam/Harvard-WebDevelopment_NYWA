# Project 1

Web Programming with Python and JavaScript


## Book Review Website: https://book-reviews-cs50-project1.herokuapp.com/

GoodReads API is used to pull in ratings from a broader audience.  

## Features:
- Users will be able to register for your website and then log in using their username and password

- search for books, leave reviews for individual books, and see the reviews made by other people. 

- users will be able to query for book details and book reviews programmatically via your website’s API.


## What did i Learn?
- Flask

- SQL to interact with Databases

- Using APIs


## :gear: Setup your own

Install all dependencies

```
$ pip install -r requirements.txt
```


Using the Webapp (for mac,use export instead of set)

```
cd <your project destination>

set FLASK_APP=application.py

set FLASK_DEBUG=1

set DATABASE_URL=postgres://dfhatankqabhkv:cdd64c7c114320146e65e2124853ee5a4638492579e4adc6c21c625aef804155@ec2-54-235-167-210.compute-1.amazonaws.com:5432/d22fa0s65eio50

set GOODREADS_KEY = yJoznQhIn56YwlQodqQ # More info: https://www.goodreads.com/api

python -m flask run

```

Have fun!
