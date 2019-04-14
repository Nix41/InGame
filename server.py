import eel
import Filters
import DBhandlers
import seed
from WebScrapping import Down_Games, Down_Movies, Down_Series

eel.init('web')

current = None

@eel.expose
def filter_series(name="", gender=[],actor="",director="", score=0, year=0, topic=""):
    if score == '':
        score = 0
    if year == '':
        year = 0
    year = int(year)
    score = int(score)
    print('*', name, '*' ,gender, '*' ,actor, '*' ,director, '*' ,score, '*' ,year)
    series = Filters.filter_series(name, gender,actor,director, score, year, topic)
    return series

@eel.expose
def filter_movies(name="", gender="",actor="",director="", score=0, year = 0, topic=""):
    if score == '':
        score = 0
    if year == '':
        year = 0
    year = int(year)
    score = int(score)
    movies = Filters.filter_movies(name, gender, actor, director, score, year, topic)
    return movies

@eel.expose
def filter_games(name = "", gender = "", launch=0, players=0,game_mode="", category="", lenguage="", score=0):
    print('n',name, 'g', gender, 'l',launch, 'p',players,'gm' ,game_mode, 'cat',category,'len',lenguage, 's', score)
    if category == 'Todos':
        category = ''
        gender=''
    if gender == 'Todos':
        gender = ''
    games = Filters.filter_games(name=name, gender=gender, launch=launch, game_mode=game_mode, category=category, lenguage=lenguage, score=score)
    print(len(games))
    return games

@eel.expose
def get_recent():
    recent = Filters.get_recent()
    return recent

@eel.expose
def CRUD_Serie(title="", year=0, pais="", sinopsis="", generos=[], directors=[], reparto=[],score=0,id=-1, image="", topics=[], delete=0):
    print(image)
    if current is None or current == -1:
        if delete == 0:
            dele = False
        else:
            dele = True
        DBhandlers.CRUD_Serie(title, year, pais, sinopsis, generos, directors, reparto, score, id, image, topics, dele)
    else:
        DBhandlers.CRUD_Serie(title, year, pais, sinopsis, generos, directors, reparto,score, current.id, image, topics, delete = False)
        Done_update()

@eel.expose
def CRUD_Movie(title="", year=0, pais="", sinopsis="", generos=[], directors=[], reparto=[],score=0, id=-1, image="", topics=[], delete=0):
    if current is None or current == -1:
        if delete == 0:
            dele = False
        else:
            dele = True
        DBhandlers.CRUD_Movie(title, year, pais, sinopsis, generos, directors, reparto, score, id, image, topics, dele)
    else:
        DBhandlers.CRUD_Movie(title, year, pais, sinopsis, generos, directors, reparto,score, current.id, image, topics, delete = False)
        Done_update()

@eel.expose
def CRUD_Game(name="", description="", game_mode="", language="", launch=0, puntuacion=0, category="", genders=[], requirements=[[],[]], id=-1, cover="", captures=[],size=0, delete=0):
    if current is None or current == -1:
        print('h2')
        if delete == 0:
            dele = False
        else:
            #qqqqqqq
            dele = True
        if len(requirements) == 0:
            print('had to')
            requirements = [[],[]]
        DBhandlers.CRUD_Game(name, description, game_mode, language, launch, puntuacion, category, genders, requirements, id, image=cover, captures=captures, size = size, delete=dele)
    else:
        print('begin_update')
        DBhandlers.CRUD_Game(name, description, game_mode, language, launch, puntuacion, category, genders, requirements, current.id, image=cover, captures=captures,size=size, delete=False)
        print('done_update')
        Done_update()

@eel.expose
def Set_Game(id):
    global current
    print('id', id )
    current = DBhandlers.find_game(id)
    print('current:' , current)

@eel.expose
def Set_Serie(id):
    print('ID:',id)
    global current
    current = DBhandlers.find_serie(id)
    print('çurrent: ', current)
@eel.expose
def Set_Movie(id):
    global current
    current = DBhandlers.find_movie(id)

@eel.expose
def Done_update():
    global current
    current = None
    print('Done update')

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
def add_tv_gender(name, typ=True):
    print('Serv: ', typ)
    DBhandlers.add_tv_gender2(current, name, typ)

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
    return seed.game_categories

@eel.expose
def get_video_genders():
    return seed.video_category

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
def download_games():
    Down_Games();

@eel.expose
def download_series():
    Down_Series();

@eel.expose
def download_movies():
    Down_Movies();

eel.start('index_vue.html')

