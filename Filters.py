 
from DBstructure import *


def get_game_genders():
    genders = []
    for gen in sess.query(GameGender).all():
        genders.append(gen.name)
    #print('genders: ',len(genders))
    return genders

def get_serie_genders():
    genders = []
    for gen in sess.query(SerieGender).all():
        genders.append(gen.name)
    return genders

def get_movie_genders():
    genders = []
    for gen in sess.query(MovieGender).all():
        genders.append(gen.name)
    return genders

def filter_games(name = "", gender = "" ):
    games = {}
    for c in sess.query(Game).filter(Game.name.contains(name)):
        genders = []
        # print()
        # print( c.launch )
        # print(c.players)
        # print(c.game_mode)
        # print(c.language)
        # print(c.puntuacion)
        # print(c.name)
        # print()
        gender_filter = False
        for g in c.genders:
            if gender in g.name:
                gender_filter = True
            genders.append(g.name)
        requirements = []
        requirements.append([])
        requirements.append([])
        for r in c.requirements:
            req = {}
            req['type'] = r.req.req_type
            req['req'] = r.req.req
            if r.minormax == True:
                requirements[0].append(req)
            else:
                requirements[1].append(req)
        if gender_filter:
            games[c.id] = {}
            games[c.id]['id'] = c.id
            games[c.id]['name'] = c.name
            games[c.id]['description'] = c.description
            games[c.id]['genders'] = genders
            games[c.id]['requirements'] = requirements
    return games

def filter_series(name = "", gender="", actor="", director=""):
    series = {}
    for s in sess.query(Serie).filter(Serie.title.contains(name)):
        genders = []
        gender_filter = False
        for g in s.genders:
            if gender in g.name:
                gender_filter = True
            genders.append(g.name)
        actor_filter  = False
        actors = []
        for a in s.actors:
            if actor in a.name:
                actor_filter = True
            actors.append(a.name)
        director_filter = False
        directors = []
        for d in s.directors:
            if director in d.name:
                director_filter = True
            directors.append(d.name)
        if gender_filter and actor_filter and director_filter:
            series[s.id] = {}
            series[s.id]['id'] = s.id
            series[s.id]['title'] = s.title
            series[s.id]['year'] = s.year 
            series[s.id]['country'] = s.sinopsis
            series[s.id]['genders'] = genders
            series[s.id]['actors'] = actors
            series[s.id]['directors'] = directors
    return series

def filter_movies(name = "", gender="", actor="", director=""):
    movies = {}
    for c in sess.query(Movie).filter(Movie.title.contains(name)):
        genders = []
        gender_filter = False
        for g in c.genders:
            if gender in g.name:
                gender_filter = True
            genders.append(g.name)
        actor_filter = False
        actors = []
        for a in c.actors:
            if actor in a.name:
                actor_filter = True
            actors.append(a.name)
        directors = []
        director_filter = False
        for d in c.directors:
            if director in d.name:
                director_filter = True
            directors.append(d.name)
        if gender_filter and actor_filter and director_filter:
            movies[c.id] = {}
            movies[c.id]['id'] = c.id
            movies[c.id]['title'] = c.title
            movies[c.id]['year'] = c.year 
            movies[c.id]['country'] = c.sinopsis
            movies[c.id]['genders'] = genders
            movies[c.id]['actors'] = actors
            movies[c.id]['directors'] = directors
    return movies

### RECUERDA AGREGAR CREATED_AT ANTES DE TESTEAR##
def get_recent():
    recent = []
    games = sess.query(Game).order_by(Game.created_at)[-3:]
    series = sess.query(Serie).order_by(Serie.created_at)[-3:]
    movies = sess.query(Movie).order_by(Movie.created_at)[-3:]
    # games = sess.query(Game).order_by(Game.id)[-3:]
    # series = sess.query(Serie).order_by(Serie.id)[-3:]
    # movies = sess.query(Movie).order_by(Movie.id)[-3:]
    for i in range(3):
        game = {}
        game['id'] = games[i].id
        game['name'] = games[i].name
        game['description'] = games[i].description
        serie = {}
        serie['id'] = series[i].id
        serie['name'] = series[i].title
        serie['description'] = series[i].sinopsis
        movie = {}
        movie['id'] = movies[i].id
        movie['name'] = movies[i].title
        movie['description'] = movies[i].sinopsis
        recent.append(game)
        recent.append(serie)
        recent.append(movie)
    return recent

def get_actors():
    actors = []
    for a in sess.query(Actor).all():
        actors.append(a.name)
    return actors

def get_directors():
    directors = []
    for d in sess.query(Director).all():
        directors.append(d.name)
    return directors