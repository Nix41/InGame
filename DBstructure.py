
# coding: utf-8


import sqlalchemy
from sqlalchemy import create_engine  
from sqlalchemy import Column, String , Integer , Table, ForeignKey, Boolean, DateTime,Float
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy.orm import sessionmaker , relationship, backref, Session
from sqlalchemy.sql import func

import re
import os
import datetime


####### WINDOWS ########
# direct = 'Work\\'
# try:
#     os.mkdir( direct)
# except: FileExistsError
# direct = 'Work\Games\\'
# try:
#     os.mkdir( direct)
# except: FileExistsError
# direct = 'Work\Movies\\'
# try:
#     os.mkdir( direct)
# except: FileExistsError
# direct = 'Work\Series\\'
# try:
#     os.mkdir( direct)
# except: FileExistsError
###########################
######### LINUX ###########
direct = 'Work/'
try:
    os.mkdir( direct)
except: FileExistsError
direct = 'Work/Games/'
try:
    os.mkdir( direct)
except: FileExistsError
direct = 'Work/Movies/'
try:
    os.mkdir( direct)
except: FileExistsError
direct = 'Work/Series/'
try:
    os.mkdir( direct)
except: FileExistsError
##########################

Base = declarative_base()

gamegen_table = Table('gamegen', Base.metadata,
    Column('game_id', Integer, ForeignKey('game.id')),
    Column('gender_id', Integer, ForeignKey('gamegender.id'))
    )

class TimestampMixin(object):
    created_at = Column(DateTime, default=func.now())

class GameGender(Base):
    __tablename__ = 'gamegender'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    games = relationship("Game", secondary=gamegen_table, backref='genders')
    
class GameReq(Base):
    __tablename__ = 'gamereq'
    left_id = Column(Integer, ForeignKey('game.id'), primary_key=True)
    right_id = Column(Integer, ForeignKey('requirement.id'), primary_key=True)
    minormax = Column(Boolean)
    game = relationship("Game", back_populates="requirements")
    req = relationship("Requirement", back_populates="games")

class Game(TimestampMixin, Base):
    __tablename__ = 'game'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    requirements = relationship("GameReq", back_populates="game")
    puntuacion = Column(Float)
    launch = Column(Integer)
    players = Column(Integer)
    game_mode = Column(String)
    language = Column(String)

class Requirement(Base):
    __tablename__ = 'requirement'
    id = Column(Integer, primary_key=True)
    req_type = Column(String)
    req = Column(String)
    games = relationship("GameReq", back_populates="req")
    
moviedir_table = Table('moviedir', Base.metadata,
    Column('movie_id', Integer, ForeignKey('movie.id')),
    Column('director_id', Integer, ForeignKey('director.id'))
    )
movieactor_table = Table('movieactor', Base.metadata,
    Column('movie_id', Integer, ForeignKey('movie.id')),
    Column('actor_id', Integer, ForeignKey('actor.id'))
    )
moviegen_table = Table('moviegen', Base.metadata,
    Column('movie_id', Integer, ForeignKey('movie.id')),
    Column('moviegender_id', Integer, ForeignKey('moviegender.id'))
    )

seriedir_table = Table('seriedir', Base.metadata,
    Column('serie_id', Integer, ForeignKey('serie.id')),
    Column('director_id', Integer, ForeignKey('director.id'))
    )
serieactor_table = Table('serieactor', Base.metadata,
    Column('serie_id', Integer, ForeignKey('serie.id')),
    Column('actor_id', Integer, ForeignKey('actor.id'))
    )
seriegen_table = Table('seriegen', Base.metadata,
    Column('serie_id', Integer, ForeignKey('serie.id')),
    Column('seriegender_id', Integer, ForeignKey('seriegender.id'))
    )
    
class Director(Base):
    __tablename__ = 'director'
    id= Column(Integer, primary_key= True)
    name = Column(String)
    movies = relationship("Movie", secondary=moviedir_table, backref='directors')
    series = relationship("Serie", secondary=seriedir_table, backref='directors')
    
class Actor(Base):
    __tablename__ = 'actor'
    id= Column(Integer, primary_key= True)
    name = Column(String)
    movies = relationship("Movie", secondary=movieactor_table, backref='actors')
    series = relationship("Serie", secondary=serieactor_table, backref='actors')
    
class MovieGender(Base):
    __tablename__ = 'moviegender'
    id= Column(Integer, primary_key= True)
    name = Column(String)
    movies = relationship("Movie", secondary=moviegen_table, backref='genders')
    
class Movie(TimestampMixin, Base):
    __tablename__ = 'movie'
    id= Column(Integer, primary_key= True)
    title = Column(String)
    year = Column(Integer)
    country = Column(String)
    sinopsis = Column(String)
    
class SerieGender(Base):
    __tablename__ = 'seriegender'
    id= Column(Integer, primary_key= True)
    name = Column(String)
    series = relationship("Serie", secondary=seriegen_table, backref='genders')

class Serie(TimestampMixin, Base):    
    __tablename__ = 'serie'
    id= Column(Integer, primary_key= True)
    title = Column(String)
    year = Column(Integer)
    country = Column(String)
    sinopsis = Column(String)

class OnExistance(Base):
    __tablename__ = 'onexistance'
    id= Column(Integer, primary_key= True)
    name = Column(String)
    tipo = Column(String)
    
e = create_engine("sqlite:///yasmany")
Base.metadata.create_all(e)

sess = Session(e)

 
