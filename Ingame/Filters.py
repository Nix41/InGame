 
from DBstructure import *
import unicodedata
import time
from sqlalchemy import and_


categories = ['']

def parse_game(c, genders):
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
    game = {}
    game['id'] = c.id
    game['name'] = c.name
    game['description'] = c.description
    game['genders'] = genders
    game['requirements'] = requirements
    game['size'] = c.size
    if not (c.category is None):
        cate = c.category.name
    else:
        cate = ''
    game['category'] = cate
    game['launch'] = c.launch
    game['game_mode'] = c.game_mode
    game['language'] = c.language
    game['score'] = c.puntuacion
    game['cover_path'] = c.cover_path
    game['captures'] = c.captures_list
    return game

def parse_tv(s, genders, actors, directors ):
    serie = {}
    serie['id'] = s.id
    serie['title'] = s.title
    serie['year'] = s.year 
    serie['sinopsis'] = s.sinopsis
    serie['country'] = s.country
    serie['genders'] = genders
    serie['actors'] = actors
    serie['directors'] = directors
    serie['score'] = s.score
    serie['cover_path'] = s.cover_path
    return serie

def get_game_genders():
    cats = {}
    for cat in sess.query(GameCategory).all():
        cats[cat.name] = []
        for g in cat.subgenders:
            cats[cat.name].append(g.name)
    ##'genders: ',len(genders))
    return cats

def get_serie_genders():
    genders = []
    for gen in sess.query(SerieGender).all():
        genders.append(gen.name)
    return genders

def get_serie_topics():
    genders = []
    for gen in sess.query(SerieTopic).all():
        genders.append(gen.name)
    return genders

def get_movie_genders():
    genders = []
    for gen in sess.query(MovieGender).all():
        genders.append(gen.name)
    return genders

def get_movie_topics():
    genders = []
    for gen in sess.query(MovieTopic).all():
        genders.append(gen.name)
    return genders

def filter_games(name = "", gender = "", launch=0, players=0,game_mode="", category="", lenguage="", score=0 , order=""):
    if launch == "":
        launch = 0
    if score == "":
        score = 0
    t = time.time()
    filter_full = sess.query(Game).filter(Game.name.contains(name)).filter(Game.launch >= launch).filter(Game.game_mode.contains(game_mode)).filter(Game.language.contains(lenguage)).filter(Game.puntuacion >= score)
    if order == 1:
        ordered = filter_full.order_by(Game.name)
    elif order == 2:
        ordered = filter_full.order_by(Game.launch.desc())
    elif order == 3:
        ordered = filter_full.order_by(Game.puntuacion.desc())
    else:
        ordered = filter_full
    for c in ordered:
        genders = []
        gender_filter = False
        for g in c.genders:
            if unicodedata.normalize('NFD', gender).encode('ascii', 'ignore').lower() in unicodedata.normalize('NFD', g.name).encode('ascii', 'ignore').lower() :
                gender_filter = True
            genders.append(g.name)
        if len(c.genders) == 0 and gender == "":
            gender_filter = True
        cat = False
        if not (c.category is None):
            cat = unicodedata.normalize('NFD', category).encode('ascii', 'ignore').lower()  in unicodedata.normalize('NFD', c.category.name).encode('ascii', 'ignore').lower() 
        else:
            cat = True
        if gender_filter and cat :
            game = parse_game(c, genders)
            yield game


def filter_series(name = "", gender=[], actor="", director="", score=0, year=0,country='', order=''):
    filter_full = sess.query(Serie).filter(Serie.title.contains(name), Serie.country.contains(country) , Serie.score >= score, Serie.year >= year)
    # prime_query = sess.query(Serie).all()
    #print('genders', gender)
    if len(gender) > 0:
        filter_full = filter_full.filter(and_(*[Serie.genders.any(SerieGender.name.contains(g)) for g in gender]))
    if actor != "":
        filter_full = filter_full.filter(Serie.actors.any(Actor.name.contains(actor)))
    if director != "":
        filter_full = filter_full.filter( Serie.directors.any(Director.name.contains(director)))
    
    if order == 1:
        ordered = filter_full.order_by(Serie.title)
    elif order == 2:
        ordered = filter_full.order_by(Serie.year.desc())
    elif order == 3:
        ordered = filter_full.order_by(Serie.score.desc())
    else:
        ordered = filter_full
    for s in ordered :
    # for s in sess.query(Serie).all():
        genders = []
        for t in s.genders:
            genders.append(t.name)
        actors = []
        for a in s.actors:
            actors.append(a.name)
        directors = []
        for d in s.directors:
            directors.append(d.name)     
        serie = parse_tv(s, genders, actors, directors)
        yield serie

def filter_movies(name = "", gender=[], actor="", director="", score=0, year=0, country="", order=''):
    filter_full = sess.query(Movie).filter(Movie.title.contains(name), Movie.country.contains(country) , Movie.score >= score, Movie.year >= year)
    if len(gender) != 0:
        filter_full = filter_full.filter(and_(*[Movie.genders.any(MovieGender.name.contains(g)) for g in gender]))
    if actor != "":
        filter_full = filter_full.filter(Movie.actors.any(Actor.name.contains(actor)))
    if director != "":
        filter_full = filter_full.filter(Movie.directors.any(Director.name.contains(director)))
        
    if order == 1:
        ordered = filter_full.order_by(Movie.title)
    elif order == 2:
        ordered = filter_full.order_by(Movie.year.desc())
    elif order == 3:
        ordered = filter_full.order_by(Movie.score.desc())
    else:
        ordered = filter_full
    for c in ordered :
        genders = []
        for t in c.genders:
            genders.append(t.name)
        actors = []
        for a in c.actors:
            actors.append(a.name)
        directors = []
        for d in c.directors:
            directors.append(d.name)
        movie = parse_tv(c, genders, actors, directors)
        yield movie

def get_recent():
    recent = []
    games = sess.query(Game).order_by(Game.created_at)[-3:]
    series = sess.query(Serie).order_by(Serie.created_at)[-3:]
    movies = sess.query(Movie).order_by(Movie.created_at)[-3:]
    g = len(games)
    s = len(series)
    m = len(movies)
    for i in range(min(g, s, m)):
        game = {}
        game['id'] = games[i].id
        game['name'] = games[i].name
        game['description'] = games[i].description
        game['src'] = games[i].cover_path
        serie = {}
        serie['id'] = series[i].id
        serie['name'] = series[i].title
        serie['description'] = series[i].sinopsis
        serie['src'] = series[i].cover_path
        movie = {}
        movie['id'] = movies[i].id
        movie['name'] = movies[i].title
        movie['description'] = movies[i].sinopsis
        movie['src'] = movies[i].cover_path
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



