import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))#create a database engine that allows python to send and recieve commands from database(from url).In this case the url is local
db = scoped_session(sessionmaker(bind=engine)) #creating sessions for diff people

def main():
    flights = db.execute("SELECT origin, destination, duration FROM flights").fetchall() #using SQL Queries. fetchall() returns all the result list
    for flight in flights:
        print(f"{flight.origin} to {flight.destination}, {flight.duration} minutes.")

if __name__ == "__main__":
    main()


