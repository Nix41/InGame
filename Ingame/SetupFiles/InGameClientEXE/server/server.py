import eel
import Filters
import DBhandlers
import seed
from urllib.error import URLError
import urllib
import subprocess 
import multiprocessing as mp
import cart

if __name__ == '__main__': 
    mp.freeze_support()
    eel.init('web')
    current = None
    to_show = []
    index = 0
    start = 0
    end = 0 
    load_amount = 25
    find_match = []
    current_process = None
    current_query = None

    @eel.expose
    def get_more(i = 1):
        global to_show
        global load_amount
        global start
        global end
        global current_query
        global  find_match
        l = len(to_show)
        # print('GOT:', i, '--', start, '--', end)
        if int(i) == 1:
            if l < end + load_amount:
                # print('h1')
                for i in range(load_amount - (l - end)):
                    try:
                        g = current_query.__next__()
                        to_show.append(g)
                        find_match.append(g['id'])
                    except StopIteration:
                        break
            l = len(to_show)
            if end != l:
                start = end
                end = min(start + load_amount, l)
        else:
            if start != 0:
                end = start
                start = max(0, start - load_amount)
        # print(len(to_show))
        return to_show[start:end]

    @eel.expose
    def next_obj(id, direction = 1):
        global to_show
        global find_match
        cui =find_match.index(id)
        if int(direction) == 1 :
            if cui == len(to_show) - 1:
                try:
                    o = current_query.__next__()
                    to_show.append(o)
                    find_match.append(o['id'])
                    return o
                except StopIteration:
                    return to_show[cui]
            else:
                return to_show[cui + 1]
        elif int(direction) != 1 and cui > 0:
            return to_show[cui - 1]

    @eel.expose
    def filter_series(name="", gender=[],actor="",director="", score=0, year=0, country=""):
        global to_show
        global index
        global start
        global end
        global find_match
        global current_query
        if score == '':
            score = 0
        if year == '':
            year = 0
        year = int(year)
        score = float(score)
        series = Filters.filter_series(name, gender,actor,director, score, year, country)
        current_query = None
        current_query = series
        find_match = []
        to_show = []
        start = 0
        end = 0
        return get_more()

    @eel.expose
    def filter_movies(name="", gender=[],actor="",director="", score=0, year = 0, country=""):
        global to_show
        global index
        global start
        global end
        global find_match
        global current_query
        if score == '':
            score = 0
        if year == '':
            year = 0
        year = int(year)
        score = float(score)
        movies = Filters.filter_movies(name, gender, actor, director, score, year, country)
        current_query = None
        current_query = movies
        to_show = []
        find_match = []
        start = 0
        end = 0
        return get_more()

    @eel.expose
    def filter_games(name = "", gender = "", launch=0, players=0,game_mode="", category="", lenguage="", score=0):
        global to_show
        global index
        global start
        global end
        global find_match
        global current_query
        if category == 'Todos':
            category = ''
            gender=''
        if gender == 'Todos':
            gender = ''
        current_query = Filters.filter_games(name=name, gender=gender, launch=launch, game_mode=game_mode, category=category, lenguage=lenguage, score=score)
        find_match = []
        to_show = []
        start = 0
        end = 0
        return get_more()

    @eel.expose
    def get_recent():
        recent = Filters.get_recent()
        return recent

    @eel.expose
    def Set_Game(id):
        global current
        #('id', id )
        current = DBhandlers.find_game(id)
        #'current Gme:' , current)

    @eel.expose
    def Set_Serie(id):
        #('ID:',id)
        global current
        current = DBhandlers.find_serie(id)
        #'çurrentS: ', current)

    @eel.expose
    def Set_Movie(id):
        global current
        current = DBhandlers.find_movie(id)
        #'çurrentM: ', current)


    @eel.expose
    def Done_update():
        global current
        current = None
        #'Done update')

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

    def try_connection():
        try:
            r = urllib.request.urlopen('http://google.com')
            return 2
        except Exception:
            print('No tienes conexion a internet, compruebe su conexion e intentelo mas tarde')
            return -1

    @eel.expose
    def get_counters():
        a = DBhandlers.get_counters()
        return a

    @eel.expose
    def add_cart_game(Id):
        cart.Add_Game(Id)

    @eel.expose
    def add_cart_serie(Id):
        cart.Add_Serie(Id)

    @eel.expose
    def add_cart_movie(Id):
        cart.Add_Movie(Id)
    
    @eel.expose
    def get_games_cart():
        return cart.get_games_cart()
    @eel.expose
    def get_series_cart():
        return cart.get_series_cart()
    @eel.expose
    def get_movies_cart():
        return cart.get_movies_cart()

    @eel.expose
    def edit_games_cart(gs):
        cart.edit_games(gs)
    @eel.expose
    def edit_series_cart(gs):
        cart.edit_series(gs)
    @eel.expose
    def edit_movies_cart(gs):
        cart.edit_movies(gs)

    eel.start('index_vue.html', options={'port':8001})


