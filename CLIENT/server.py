import eel
import Filters
import seed

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
def filter_movies(name="", gender=[],actor="",director="", score=0, year = 0, topic=""):
    if score == '':
        score = 0
    if year == '':
        year = 0
    year = int(year)
    score = int(score)
    print('*', name, '*' ,gender, '*' ,actor, '*' ,director, '*' ,score, '*' ,year)
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



eel.start('index_vue.html')

