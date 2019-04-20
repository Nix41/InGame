 
from DBstructure import *
import unicodedata
import time

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
    games = []
    if launch == "":
        launch = 0
    if score == "":
        score = 0
    # if gender is None:
    #     gender = ""
    t = time.time()
    print('Before filter: ', t)
    filter_full = sess.query(Game).filter(Game.name.contains(name)).filter(Game.launch >= launch).filter(Game.game_mode.contains(game_mode)).filter(Game.language.contains(lenguage)).filter(Game.puntuacion >= score)
    e = time.time()
    print('After filter: ', time.time() - t)
    t = e
    for c in filter_full:
        genders = []
        # #'**')
         #(c.name)
        # #c.category.name)
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
            games.append(game)
    print('After Process: ', time.time() - t)
    return games


def filter_series(name = "", gender=[], actor="", director="", score=0, year=0,topic=''):
    series = []
    for s in sess.query(Serie).filter(Serie.title.contains(name)):
    # for s in sess.query(Serie).all():
        print(s.title)
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
            c_gen = unicodedata.normalize('NFD', gen).encode('ascii', 'ignore')
            for g in s.genders:
                c_g = unicodedata.normalize('NFD', g.name).encode('ascii', 'ignore')
                if c_gen.lower() in c_g.lower():
                    #s.title)
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
            if unicodedata.normalize('NFD', actor).encode('ascii', 'ignore').lower() in unicodedata.normalize('NFD', a.name).encode('ascii', 'ignore').lower() :
                actor_filter = True
            actors.append(a.name)
        director_filter = False
        directors = []
        for d in s.directors:
            if unicodedata.normalize('NFD', director).encode('ascii', 'ignore').lower()  in unicodedata.normalize('NFD', d.name).encode('ascii', 'ignore').lower() :
                director_filter = True
            directors.append(d.name)
        if gender_filter and actor_filter and director_filter and s.score >= score and topic_filter and s.year >= year:
            serie = {}
            serie['id'] = s.id
            serie['title'] = s.title
            serie['year'] = s.year 
            serie['topics'] = stopics
            serie['sinopsis'] = s.sinopsis
            serie['country'] = s.country
            serie['genders'] = genders
            serie['actors'] = actors
            serie['directors'] = directors
            serie['score'] = s.score
            print('Bcover')
            serie['cover_path'] = s.cover_path
            print('Acover')
            series.append(serie)
    return series

def filter_movies(name = "", gender=[], actor="", director="", score=0, year=0, topic=""):
    movies = []
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
                if unicodedata.normalize('NFD', gen).encode('ascii', 'ignore').lower()  in unicodedata.normalize('NFD', g.name).encode('ascii', 'ignore').lower() :
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
            if unicodedata.normalize('NFD', actor).encode('ascii', 'ignore').lower() in unicodedata.normalize('NFD', a.name).encode('ascii', 'ignore').lower() :
                actor_filter = True
            actors.append(a.name)
        directors = []
        director_filter = False
        for d in c.directors:
            if unicodedata.normalize('NFD', director).encode('ascii', 'ignore').lower()  in unicodedata.normalize('NFD', d.name).encode('ascii', 'ignore').lower() :
                director_filter = True
            directors.append(d.name)
        if gender_filter and actor_filter and director_filter and c.score >= score and topic_filter and c.year >= year:
            movie = {}
            movie['id'] = c.id
            movie['title'] = c.title
            movie['year'] = c.year 
            movie['topics'] = stopics
            movie['sinopsis'] = c.sinopsis
            movie['country'] = c.country
            movie['genders'] = genders
            movie['actors'] = actors
            movie['directors'] = directors
            movie['score'] = c.score
            movie['cover_path'] = c.cover_path
            movies.append(movie)
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

# filter_games()

# s
# filter_series()
# filter_movies()



