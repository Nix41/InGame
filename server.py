import eel
import Filters
import DBhandlers
import seed
from WebScrapping import Down_Games, Down_Movies, Down_Series
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
    def CRUD_Serie(title="", year=0, pais="", sinopsis="", generos=[], directors=[], reparto=[],score=0,id=-1, image="", topics=[], delete=0):
        #(image)
        if current is None or current == -1:
            if delete == 0:
                dele = False
            else:
                dele = True
            if year == '':
                year = 0
            if score == '':
                score = 0
            DBhandlers.CRUD_Serie(title, year, pais, sinopsis, generos, directors, reparto, score, id, image, topics, dele)
        else:
            if year == '':
                year = 0
            if score == '':
                score = 0
            DBhandlers.CRUD_Serie(title, year, pais, sinopsis, generos, directors, reparto,score, current.id, image, topics, delete = False)
            Done_update()

    @eel.expose
    def CRUD_Movie(title="", year=0, pais="", sinopsis="", generos=[], directors=[], reparto=[],score=0, id=-1, image="", topics=[], delete=0):
        if current is None or current == -1:
            if delete == 0:
                dele = False
            else:
                dele = True
            if year == '':
                year = 0
            if score == '':
                score = 0
            DBhandlers.CRUD_Movie(title, year, pais, sinopsis, generos, directors, reparto, score, id, image, topics, dele)
        else:
            if year == '':
                year = 0
            if score == '':
                score = 0
            DBhandlers.CRUD_Movie(title, year, pais, sinopsis, generos, directors, reparto,score, current.id, image, topics, delete = False)
            Done_update()

    @eel.expose
    def CRUD_Game(name="", description="", game_mode="", language="", launch=0, puntuacion=0, category="", genders=[], requirements=[[],[]], id=-1, cover="", captures=[],size=0, delete=0):
        #'here')
        global current
        if current is None or current == -1:
            #'here222')
            #'h2')
            if delete == 0:
                dele = False
            else:
                #qqqqqqq
                dele = True
            if len(requirements) == 0:
                #('had to')
                requirements = [[],[]]
            if puntuacion == '':
                puntuacion = 0
            #'DEl:', dele)
            DBhandlers.CRUD_Game(name, description, game_mode, language, launch, puntuacion, category, genders, requirements, id, image=cover, captures=captures, size = size, delete=dele)
        else:
            if puntuacion == '':
                puntuacion = 0
            #'current: ', current)
            #('begin_update')
            #'WTF???????')
            #current)
            DBhandlers.CRUD_Game(name, description, game_mode, language, launch, puntuacion, category, genders, requirements, current.id, image=cover, captures=captures,size=size, delete=False)
            #('done_update')
            Done_update()

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
        #('Serv: ', typ)
        DBhandlers.add_tv_gender2(current, name, typ)

    @eel.expose
    def del_tv_gender(name):
        DBhandlers.del_tv_gender(current, name)

    @eel.expose
    def add_topic(name):
        DBhandlers.add_topic2(current, name)

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

    def try_connection():
        try:
            r = urllib.request.urlopen('http://google.com')
            return 2
        except Exception:
            print('No tienes conexion a internet, compruebe su conexion e intentelo mas tarde')
            return -1

    @eel.expose
    def download_games():
        global current_process
        if current_process is None or not(current_process.is_alive()):
            r = try_connection()
            print('Con:',r)
            if r == 2:
                current_process = downgames()
            return r
        else:
            print('Espera a que terminen Los demas procesos y vuelvalo a intentar')
            return 0

    @eel.expose
    def download_series():
        global current_process
        if current_process is None or not(current_process.is_alive()):
            r = try_connection()
            if r == 2:
                current_process = downseries()
            return r
        else:
            print('Espera a que terminen Los demas procesos y vuelvalo a intentar')
            return 0

    @eel.expose
    def download_movies():
        global current_process
        if current_process is None or not(current_process.is_alive()):
            r = try_connection()
            print('Con:',r)
            if r == 2:
                current_process = downmovies()
            return r
        else:
            print('Espera a que terminen Los demas procesos y vuelvalo a intentar')
            return 0

    @eel.expose
    def gen_pdf():
        subprocess.run('python pdf.py')

    @eel.expose
    def get_counters():
        a = DBhandlers.get_counters()
        return a

    @eel.expose
    def kill_download():
        global current_process
        if not (current_process is None):
            current_process.terminate()
            current_process.join()
            current_process = None
            print('Ha sido detenida la descarga')

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

    def downgames():
        current_process = mp.Process(target= Down_Games)
        current_process.start()
        return current_process

    def downseries():
        current_process = mp.Process(target= Down_Series)
        current_process.start()
        return current_process

    def downmovies():
        current_process = mp.Process(target= Down_Movies)
        current_process.start()
        return current_process

    eel.start('index_vue.html')


