import eel
import Filters
import DBhandlers


eel.init('web')

current = None

@eel.expose
def filter_series(name="", gender="",actor="",director="", score=0):
    series = Filters.filter_series(name, gender,actor,director, score)
    return series

@eel.expose
def filter_movies(name="", gender="",actor="",director="", score=0):
    movies = Filters.filter_movies(name, gender, actor, director, score)
    return movies

@eel.expose
def filter_games(name = "", gender = "", launch=0, players=0,game_mode="", category="", lenguage="", score=0):
    games = Filters.filter_games(name=name, gender=gender, launch=launch, game_mode=game_mode, category=category, lenguage=lenguage, score=score)
    return games

@eel.expose
def get_recent():
    recent = Filters.get_recent()
    return recent

@eel.expose
def CRUD_Serie(title="", year=0, pais="", sinopsis="", generos=[], directors=[], reparto=[],id=-1, image="", delete=False):
    if current is None or current == -1:
        DBhandlers.CRUD_Serie(title, year, pais, sinopsis, generos, directors, reparto, id, image, delete)
    else:
        DBhandlers.CRUD_Serie(title, year, pais, sinopsis, generos, directors, reparto, current.id, image, delete)
        Done_update()

@eel.expose
def CRUD_Movie(title="", year=0, pais="", sinopsis="", generos=[], directors=[], reparto=[],id=-1, image="", delete=False):
    if current is None or current == -1:
        DBhandlers.CRUD_Movie(title, year, pais, sinopsis, generos, directors, reparto, id, image, delete)
    else:
        DBhandlers.CRUD_Movie(title, year, pais, sinopsis, generos, directors, reparto, current.id, image, delete)
        Done_update()

@eel.expose
def CRUD_Game(name="", description="", game_mode="", language="", launch=0, puntuacion=0, category="", genders=[], requirements=[], id=-1, cover="", captures=[], delete=False):
    print('h1')
    print(cover)
    print(name)
    if current is None or current == -1:
        print('h2')
        DBhandlers.CRUD_Game(name, description, game_mode, language, launch, puntuacion, category, genders, requirements, id, image=cover, captures=captures, delete=delete)
    else:
        print('h3')
        DBhandlers.CRUD_Game(name, description, game_mode, language, launch, puntuacion, category, genders, requirements, current.id, image=cover, captures=captures, delete=delete)
        Done_update()

@eel.expose
def Set_Game(id):
    global current
    current = DBhandlers.find_game(id)
@eel.expose
def Set_Serie(id):
    global current
    current = DBhandlers.find_serie(id)
@eel.expose
def Set_Movie(id):
    global current
    current = DBhandlers.find_movie(id)

@eel.expose
def Done_update():
    global current
    current = None

@eel.expose
def add_director(name):
    DBhandlers.add_director2(current, name)

@eel.expose
def del_director(name):
    DBhandlers.del_director(current, name)

@eel.expose
def add_actor(name):
    DBhandlers.add_actor2(current, name)

@eel.expose
def del_actor(name):
    DBhandlers.del_actor(current, name)

@eel.expose
def add_tv_gender(name):
    DBhandlers.add_tv_gender2(current, name)

@eel.expose
def del_tv_gender(name):
    DBhandlers.del_tv_gender(current, name)

@eel.expose
def add_topic(name):
    DBhandlers.add_topic(current, name)

@eel.expose
def del_topic(name):
    DBhandlers.del_topic(current, name)

@eel.expose
def add_game_gender(name):
    DBhandlers.add_game_gender(current, name)

@eel.expose
def del_game_gender(name):
    DBhandlers.del_game_gender(current, name)

@eel.expose
def get_game_genders():
    return Filters.get_game_genders()

@eel.expose
def get_serie_genders():
    return Filters.get_serie_genders()

@eel.expose
def get_serie_topics():
    return Filters.get_serie_topics()

@eel.expose
def get_movie_genders():
    return Filters.get_movie_genders()

@eel.expose
def get_movie_topics():
    return Filters.get_movie_topics()

@eel.expose
def get_downloads():
    return DBhandlers.get_downloads()

@eel.expose
def set_downloads(txt):
    DBhandlers.set_downloads(txt)

eel.start('index_vue.html')

