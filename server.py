import eel
import Filters
import DBhandlers

eel.init('web')

@eel.expose
def filter_series(name="", gender="",actor="",director=""):
    series = Filters.filter_series(name, gender,actor,director)
    return series

@eel.expose
def filter_movies(name="", gender="",actor="",director=""):
    movies = Filters.filter_movies(name, gender, actor, director)
    return movies

@eel.expose
def filter_games(name="", gender=""):
    games = Filters.filter_games(name, gender)
    return games

@eel.expose
def get_recent():
    recent = Filters.get_recent()
    return recent

eel.start('index.html')
