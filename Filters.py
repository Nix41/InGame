 
from DBstructure import *

categories = ['']

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

def match_games(game , name = "", gender = "", launch=0, players=0,game_mode="", category="", lenguage="", score=0):
    match_all = True
    # if not((name in game.name) and (game_mode in game.game_mode) and (category == game.category.name) and (lenguage in game.lenguage) and (score <= game.score) and (launch >= game.launch)):
    if not((game.name.contains(name)) and (game.game_mode.contains(game_mode)) and (game.category.name.contains(category)) and (game.lenguage.contains(lenguage)) and (score <= game.score) and (launch >= game.launch)):
        match_all = False
        return False
    if not(players >= game.min_players and players <= game.max_players):
        match_all = False
        return False
    gender = False
    for g in game.genders:
        if gender in g.name:
            gender = True
    match_all = gender
    return match_all
    

def filter_games(name = "", gender = "", launch=0, players=0,game_mode="", category="", lenguage="", score=0 ):
    games = {}
    for c in sess.query(Game).filter(Game.name.contains(name)).filter(Game.launch > launch).filter(Game.game_mode.contains(game_mode)).filter(Game.language.contains(lenguage)).filter(Game.puntuacion >= score):
        print(c.name)
        print(c.cover_path)
        print(c.captures)
        genders = []
        gender_filter = False
        for g in c.genders:
            if gender in g.name:
                gender_filter = True
            genders.append(g.name)
        if gender_filter and category in c.category.name :
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
            games[c.id] = {}
            games[c.id]['id'] = c.id
            games[c.id]['name'] = c.name
            games[c.id]['description'] = c.description
            games[c.id]['genders'] = genders
            games[c.id]['requirements'] = requirements
            games[c.id]['size'] = c.size
            games[c.id]['category'] = c.category.name
            games[c.id]['launch'] = c.launch
            games[c.id]['game_mode'] = c.game_mode
            games[c.id]['language'] = c.language
            games[c.id]['score'] = c.puntuacion
            games[c.id]['cover_path'] = c.cover_path
            games[c.id]['captures'] = c.captures
    return games

def filter_series(name = "", gender="", actor="", director=""):
    series = {}
    for s in sess.query(Serie).filter(Serie.title.contains(name)):
        genders = []
        print(s.title)
        print(s.score)
        print(s.id)
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
        print(c.title)
        print(c.score)
        print(c.id)
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
    # series = sess.query(Serie).order_by(Serie.created_at)[-3:]
    movies = sess.query(Movie).order_by(Movie.created_at)[-3:]
    # games = sess.query(Game).order_by(Game.id)[-3:]
    series = sess.query(Serie).order_by(Serie.id)[-3:]
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

# filter_games()
# filter_series()
# filter_movies()
