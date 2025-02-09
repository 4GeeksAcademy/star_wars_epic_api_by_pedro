from flask_sqlalchemy import SQLAlchemy
import enum
db = SQLAlchemy()

import os
import sys

from enum import Enum
from sqlalchemy import ForeignKey, Integer, String
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass
from random import randint

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/test.db"
app.config["SQLALCHEMY_ECHO"] = True
db = SQLAlchemy(app)

@dataclass
class Character(db.Model):
    __tablename__ = 'character'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id:int = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name:str = db.Column(db.String(250), nullable=False)
    firstname:str = db.Column(db.String(250), nullable=False)
    home_world:int = db.Column(db.Integer,ForeignKey('planet.id'), nullable=False)
    species:int = db.Column(db.Integer, ForeignKey('species.id'),nullable=False)

@dataclass
class Planet(db.Model):
    __tablename__ = 'planet'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id:int= db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name:str = db.Column(db.String(250), nullable=False)
    population:int=db.Column(db.Integer,nullable=False )


@dataclass
class Species(db.Model):
    __tablename__ = 'species'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id:int= db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name:str = db.Column(db.String(250), nullable=False)
    homeworld:int=db.Column(db.Integer,ForeignKey('planet.id'),nullable=False )
    language:str=db.Column(db.String(250), nullable=False)

@dataclass
class User(db.Model):
    __tablename__ = 'user'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id:int= db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name:str = db.Column(db.String(250), nullable=False)
    password:str=db.Column(db.String(250),nullable=False )
    email:str=db.Column(db.String(250), nullable=False, unique=True)


class FavoriteTypeEnum(str,Enum):
    planet="planet"
    character="character"
    species="species"



@dataclass
class Favourite_list(db.Model):
    __tablename__ = 'favourites'
    id: int = db.Column(db.Integer, primary_key=True, nullable=False)
    external_id: int = db.Column(db.Integer, nullable=False)
    type: str = db.Column(db.Enum(FavoriteTypeEnum), nullable=False)
    name: str = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Favourite {self.name}>'



    # def __repr__(self):
    #     return '<User %r>' % self.username

    # def serialize(self):
    #     return {
    #         "id": self.id,
    #         "email": self.email,
    #         # do not serialize the password, its a security breach
    #     }


