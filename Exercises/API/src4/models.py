from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Flight(db.Model): #using objects to interact with database 
    __tablename__ = "flights" #name of the table
    id = db.Column(db.Integer, primary_key=True) 
    origin = db.Column(db.String, nullable=False) #origin,string that is not null
    destination = db.Column(db .String, nullable=False)
    duration = db.Column(db.Integer, nullable=False)


class Passenger(db.Model):
    __tablename__ = "passengers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    flight_id = db.Column(db.Integer, db.ForeignKey("flights.id"), nullable=False)#foreign key meaning referencing another table column

