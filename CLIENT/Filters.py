 
from DBstructure import *

categories = ['']

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

def filter_games(name = "", gender = "", launch=0, players=0,game_mode="", category="", lenguage="", score=0 ):
    games = {}
    if launch == "":
        launch = 0
    if score == "":
        score = 0
    # if gender is None:
    #     gender = ""
    for c in sess.query(Game).filter(Game.name.contains(name)).filter(Game.launch >= launch).filter(Game.game_mode.contains(game_mode)).filter(Game.language.contains(lenguage)).filter(Game.puntuacion >= score):
    # for c in sess.query(Game).all():
        genders = []
        # #'**')
        # #c.category.name)
        gender_filter = False
        for g in c.genders:
            if gender in g.name:
                gender_filter = True
            genders.append(g.name)
        if len(c.genders) == 0 and gender == "":
            gender_filter = True
        cat = False
        if not (c.category is None):
            cat = category in c.category.name
        else:
             #('NO CATEGORY ')
            cat = True
        if gender_filter and cat :
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
            if not (c.category is None):
                cate = c.category.name
            else:
                cate = ''
            games[c.id]['category'] = cate
            games[c.id]['launch'] = c.launch
            games[c.id]['game_mode'] = c.game_mode
            games[c.id]['language'] = c.language
            games[c.id]['score'] = c.puntuacion
            games[c.id]['cover_path'] = c.cover_path
            games[c.id]['captures'] = c.captures_list
    return games

def filter_series(name = "", gender=[], actor="", director="", score=0, year=0,topic=''):
    series = {}
    for s in sess.query(Serie).filter(Serie.title.contains(name)):
    # for s in sess.query(Serie).all():
        stopics = []
        gender_filter = False
        for t in s.topics:
            if topic in t.name:
                gender_filter = True
            stopics.append(t.name)
        if not(s.topics):
            gender_filter = True
        topic_filter  = True
        for gen in gender:
            this_topic = False
            for g in s.genders:
                if gen in g.name:
                    this_topic = True
            if not this_topic:
                topic_filter = False
                break
             #(topic_filter)
        genders = []
        for t in s.genders:
            genders.append(t.name)
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
        if gender_filter and actor_filter and director_filter and s.score >= score and topic_filter and s.year >= year:
            series[s.id] = {}
            series[s.id]['id'] = s.id
            series[s.id]['title'] = s.title
            series[s.id]['year'] = s.year 
            series[s.id]['topics'] = stopics
            series[s.id]['sinopsis'] = s.sinopsis
            series[s.id]['country'] = s.country
            series[s.id]['genders'] = genders
            series[s.id]['actors'] = actors
            series[s.id]['directors'] = directors
            series[s.id]['score'] = s.score
            series[s.id]['cover_path'] = s.cover_path
    return series

def filter_movies(name = "", gender=[], actor="", director="", score=0, year=0, topic=""):
    movies = {}
    for c in sess.query(Movie).filter(Movie.title.contains(name)):
        stopics = []
        gender_filter = False
        for t in c.topics:
            if topic in t.name:
                gender_filter = True
            stopics.append(t.name)
        if not(c.topics):
            gender_filter = True
        topic_filter  = True
        for gen in gender:
            this_topic = False
            for g in c.genders:
                if gen in g.name:
                    this_topic = True
            if not this_topic:
                topic_filter = False
                break
             #(topic_filter)
        genders = []
        for t in c.genders:
            genders.append(t.name)
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
        if gender_filter and actor_filter and director_filter and c.score >= score and topic_filter and c.year >= year:
            movies[c.id] = {}
            movies[c.id]['id'] = c.id
            movies[c.id]['title'] = c.title
            movies[c.id]['year'] = c.year 
            movies[c.id]['topics'] = stopics
            movies[c.id]['sinopsis'] = c.sinopsis
            movies[c.id]['country'] = c.country
            movies[c.id]['genders'] = genders
            movies[c.id]['actors'] = actors
            movies[c.id]['directors'] = directors
            movies[c.id]['score'] = c.score
            movies[c.id]['cover_path'] = c.cover_path
    return movies

### RECUERDA AGREGAR CREATED_AT ANTES DE TESTEAR##
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



