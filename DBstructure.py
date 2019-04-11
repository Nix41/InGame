
# coding: utf-8


import sqlalchemy
from sqlalchemy import create_engine  
from sqlalchemy import Column, String , Integer , Table, ForeignKey, Boolean, DateTime,Float
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy.orm import sessionmaker , relationship, backref, Session
from sqlalchemy.sql import func
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method

import re
import os
import datetime

####### WINDOWS ########
# slash = '\\'
###########################
######### LINUX ###########
slash = '\\'

MAIN_DIRECTORY = 'web'+ slash + 'img' + slash+ 'Work' + slash 
games_dir = MAIN_DIRECTORY + 'Games' + slash
series_dir = MAIN_DIRECTORY + 'Series' + slash
movies_dir = MAIN_DIRECTORY + 'Movies' + slash

g_list = 'lists' + slash + 'games.txt'
m_list = 'lists' + slash + 'movies.txt'
s_list = 'lists' + slash + 'series.txt'

direct = MAIN_DIRECTORY
# try:
#     os.mkdir( direct)
# except: FileExistsError
# try:
#     os.mkdir( games_dir)
# except: FileExistsError
# try:
#     os.mkdir( series_dir)
# except: FileExistsError
# try:
#     os.mkdir( series_dir)
# except: FileExistsError

Base = declarative_base()

gamegen_table = Table('gamegen', Base.metadata,
    Column('game_id', Integer, ForeignKey('game.id')),
    Column('gender_id', Integer, ForeignKey('gamegender.id'))
    )

class TimestampMixin(object):
    created_at = Column(DateTime, default=func.now())

class GameCategory(Base):
    __tablename__ = 'gamecategory'
    id = Column(Integer, primary_key=True)
    name = Column(String)

class GameGender(Base):
    __tablename__ = 'gamegender'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    games = relationship("Game", secondary=gamegen_table, backref='genders')
    category_id = Column(Integer, ForeignKey('gamecategory.id'))
    category = relationship("GameCategory", backref=backref('subgenders'))

class GameReq(Base):
    __tablename__ = 'gamereq'
    left_id = Column(Integer, ForeignKey('game.id'), primary_key=True)
    right_id = Column(Integer, ForeignKey('requirement.id'), primary_key=True)
    minormax = Column(Boolean)
    game = relationship("Game", single_parent=True , cascade='save-update, delete, delete-orphan',back_populates="requirements")
    req = relationship("Requirement",single_parent=True , back_populates="games")

class Game(TimestampMixin, Base):
    __tablename__ = 'game'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    requirements = relationship("GameReq", back_populates="game")
    puntuacion = Column(Float)
    launch = Column(Integer)
    game_mode = Column(String)
    language = Column(String)
    min_players = Column(Integer)
    max_players = Column(Integer)
    category_id = Column(Integer, ForeignKey('gamecategory.id'))
    category = relationship("GameCategory", backref=backref('games'))
    size = Column(Integer)

    @hybrid_property
    def cover_path(self):
        return (games_dir[4:] + str(self.id) + 'image.jpeg')
    @hybrid_property
    def cover_direct(self):
        return os.getcwd() + slash + games_dir + self.id 
    @hybrid_property
    def captures_list(self):
        caps = []
        for r, d, f in os.walk(games_dir + str(self.id) + slash):
            for file in f:
                caps.append(os.path.join(r, file)[4:])
        return caps

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
movietop_table = Table('movietop', Base.metadata,
    Column('movie_id', Integer, ForeignKey('movie.id')),
    Column('movietopic_id', Integer, ForeignKey('movietopic.id'))
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
serietop_table = Table('serietop', Base.metadata,
    Column('serie_id', Integer, ForeignKey('serie.id')),
    Column('serietopic_id', Integer, ForeignKey('serietopic.id'))
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

class MovieTopic(Base):
    __tablename__ = 'movietopic'
    id= Column(Integer, primary_key= True)
    name = Column(String)
    movies = relationship("Movie", secondary=movietop_table, backref='topics')
    
class Movie(TimestampMixin, Base):
    __tablename__ = 'movie'
    id= Column(Integer, primary_key= True)
    title = Column(String)
    year = Column(Integer)
    country = Column(String)
    sinopsis = Column(String)
    score = Column(Float)
    @hybrid_property
    def cover_path(self):
        print(movies_dir[4:] + str(self.id) + 'image.jpeg')
        return (movies_dir[4:] + str(self.id) + 'image.jpeg')
    @hybrid_property
    def cover_direct(self):
        return os.getcwd() + slash +games_dir + self.id 
    
class SerieGender(Base):
    __tablename__ = 'seriegender'
    id= Column(Integer, primary_key= True)
    name = Column(String)
    series = relationship("Serie", secondary=seriegen_table, backref='genders')

class SerieTopic(Base):
    __tablename__ = 'serietopic'
    id= Column(Integer, primary_key= True)
    name = Column(String)
    series = relationship("Serie", secondary=serietop_table, backref='topics')

class Serie(TimestampMixin, Base):
    __tablename__ = 'serie'
    id= Column(Integer, primary_key= True)
    title = Column(String)
    year = Column(Integer)
    country = Column(String)
    sinopsis = Column(String)
    score = Column(Float)
    @hybrid_property
    def cover_path(self):
        return (series_dir[4:] + str(self.id) + 'image.jpeg')
    @hybrid_property
    def cover_direct(self):
        return os.getcwd() + slash + games_dir + self.id 

class OnExistance(Base):
    __tablename__ = 'onexistance'
    id= Column(Integer, primary_key= True)
    name = Column(String)
    tipo = Column(String)
    
e = create_engine("sqlite:///yasmany")
Base.metadata.create_all(e)

sess = Session(e)

# delete_games = Game.__table__.delete()
# sess.execute(delete_games)

# delete_existance = OnExistance.__table__.delete()
# sess.execute(delete_existance)

