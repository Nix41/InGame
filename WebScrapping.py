
from DBstructure import *
from DBhandlers import *
from utils import clean
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import urllib.request
from selenium.webdriver.common.by import By

tracks = 0
def track():
    global tracks
    print('TRACK ==> ', tracks)
    tracks += 1

def get_captures(game, ids):
    i = 0
    #WINDOWS#
    #dirt = 'web\img\Work\Games\\' + str(ids)
    #UBUNTU
    dirt = 'web/img/Work/Games/' + str(ids)
    try:
        os.mkdir( dirt)
    except: FileExistsError
        
    for im in game.findAll('img', class_='wi100'):
        #WINDOWS
        #with urllib.request.urlopen(im['data-src']) as response, open(dirt + '\image' + str(i) + '.jpeg', 'wb') as out_file:
        #UBUNTU
        with urllib.request.urlopen(im['data-src']) as response, open(dirt + '/image' + str(i) + '.jpeg', 'wb') as out_file:
            data = response.read()
            out_file.write(data)
        i = i + 1

def gen_requisitos(gameurl):
    i = 0
    for k in range(len(gameurl)):
        if gameurl[k] == '/':
            i = i + 1
            if(i == 3):
                req = gameurl[:k] + '/juegos/requisitos' + gameurl[k:]
                return req
     
def extract_req(req, game, boo):
    print(req)
    space_key = ['Almacenamiento', 'Disco', 'Duro', 'Espacio', 'almacenamiento', 'disco', 'duro', 'espacio']
    sep = re.split(': | \(' , req)
    print(sep)
    if len(sep) > 1:
        # print('h1')
        reqd = Requirement(req_type = sep[0] , req = sep[1])
    else: 
        # print('h2')
        reqd = Requirement(req_type = "" , req = sep[0])

    if boo == 0:
        # print('h3')
        gr = GameReq(req = reqd, minormax = False)
    else:
        # print('h4')
        gr = GameReq(req = reqd, minormax = True)
    # print('#################################################################')
    print(sep[0])
    for key in space_key:
        if key in sep[0]:
            # print('--> ', key, ' in ', sep[0] )
            size = 0
            # print(sep[1])
            p = re.compile(r'\d+')
            st = p.findall(sep[1])
            if len(st) > 0:
                print(st[0])
                size = st[0]
            # print('SIZE : ',size)
            game.size = size
            break
    game.requirements.append(gr)
    
def requisitos(url, game):
    req = urllib .request.urlopen(url)
    soup = BeautifulSoup(req)
    soup.prettify()
    first = True
    category = None
    for gender in soup.find_all('a', href=re.compile('.*juegos-generos.*')):
        gender_name = gender.get_text()
        if not('juego' in gender_name):
            # print(gender_name)
            if first:
                first = False
                category = find_category(gender_name)
                game.category = category
            else:
                add_gender_to_game(game, gender_name, category)
    regex = re.compile('.*list_foro.*')
    reqs = soup.find_all(class_= regex)
    i = 0
    # print('QQQQQQQQQQQQQQQQQQQQQQQQQQQ')
    for gr in reqs:
        # print(str(i))
        for lis in gr.find_all('li'):
            # print(str(lis.get_text()))
            extract_req(lis.get_text(), game, i)
        i = i + 1
    
    print('next')

def find_games(sourcelist):
    urlstart = 'https://www.3djuegos.com/?q='
    urlend = '&zona=resultados-buscador&id_foro=0&subzona=juegos&id_plat=1'
    games = []
    not_found = ''
    
    with open(sourcelist , "r") as std:
        games = std.readlines()

    for g in games:
        s = re.sub( ' +', ' ', g ).strip()
        already = sess.query(OnExistance).filter(OnExistance.name == g, OnExistance.tipo == 'Game')
        if already.count() == 0:
            one = OnExistance(name = g, tipo = 'Game')
            sess.add_all([one])
            sess.commit()
            s = s.replace(' ' , '+')
            url = urlstart + s + urlend
            print(url)
            driver = webdriver.PhantomJS()
            driver.get(url)
            try:
                resp = driver.find_element_by_xpath('//*[@class="xXx b"]')
                # print('aaaaaa')
                # resp = driver.find_element_by_css_selector('.xXx.b')
                # print(resp, 'wwwwwwwwwwwww')
                # print(resp.get_attribute('href'))
                s = resp.get_attribute('href')
                # print('QQ   ', s)
                game = urllib.request.urlopen(s).read()
                 #1
                soup_game = BeautifulSoup(game)
                 #2
                soup_game.prettify()
                 #3
                game_name = soup_game.title.string
                 #4
                description = "" +soup_game.select_one("#adpepito").get_text()
                jname = game_name[:-18]
                 #5
                here = sess.query(Game).filter(Game.name == jname)
                 #6
                p_element = soup_game.find(class_='pr t6')
                 #7
                if p_element is None:
                    puntuacion = 0
                     #8
                else:
                     #9
                    puntuacion_str = re.split(',', soup_game.find(class_='pr t6').get_text())
                    puntuacion = 0
                     #10
                    for i in range(len(puntuacion_str)):
                        puntuacion += (int)(puntuacion_str[i]) * (10**(-i))
                        # print('*********',puntuacion, "***")
                     #11
                language=""
                for head in soup_game.find_all('dt'):
                     #12
                    typ = head.get_text()
                    prop = head.find_next('dd').get_text()
                     #13
                    if 'Lanzamiento' in typ :
                         #14
                        date_str = re.split(' ', prop)
                        year = 0
                        for date in date_str:
                            try:
                                year = int(date)
                            except: Exception
                            if year > 1000:
                                break
                        launch = year                       
                    if 'Jugadores' in typ:
                         #15
                        game_type = prop
                    if 'Idioma' in typ:
                        print('!!!!!!!!!!!!!!!!!!!!!!!!Language:    ')
                         #16
                        print(prop)
                        language = prop                  
                if here.count() == 0:
                    print('#',language,'#')
                    this_game = Game(name = jname, description= description, game_mode =game_type, language= language, launch= launch, puntuacion = puntuacion )  
                    req = gen_requisitos(s)
                    # print('HERE')
                    requisitos(req, this_game)  
                     
                    sess.add_all([this_game])
                     
                    sess.commit()
                     
                    get_captures(soup_game , this_game.id)
                    image = soup_game.find(rel='image_src')
                    # print('****************')
                    im = image['href']
                    # print(im)
 #                   with urllib.request.urlopen(im) as response, open('web\img\Work\Games\\' + str(this_game.id) + 'image.jpeg', 'wb') as out_file:
                    with urllib.request.urlopen(im) as response, open('web/img/Work/Games/' + str(this_game.id) + 'image.jpeg', 'wb') as out_file: 
                        data = response.read()
                        out_file.write(data)
            except NoSuchElementException:
                not_found += (g + '\n')
                print('it does not exist')
        else:
            print('ya has hecho esta busqueda ' + g)
    #WINDOW
    #with open('web\img\Work\Games\\notfound.txt' , 'at') as std:
    #UBUNTU
    with open('web/img/Work/Games/notfound.txt' , 'at') as std:
        std.write(not_found)          

def extract_info(url, build_method):
    url = 'https://www.filmaffinity.com' + url
    mov = urllib.request.urlopen(url)
    movsoup = BeautifulSoup(mov)
    movsoup.prettify()
    info = movsoup.find(class_='movie-info')
    name = ''
    generos = []
    reparto = []
    directors = []
    sinopsis = ''
    anno = ''
    pais = ''
    for head in info.find_all('dt'):
        typ = head.get_text()
        prop = head.find_next('dd').get_text()
        if 'Título original' in typ :
            name = re.sub( '\s+', ' ', prop ).strip()
        if 'Género' in typ :
            generos = re.split('\\|' , re.sub( '\s+', ' ', prop ).strip() )
        if 'Reparto' in typ :
            reparto = re.split(',' , re.sub( '\s+', ' ', prop ).strip())
        if 'Sinopsis' in typ :
            sinopsisa = re.sub( '\s+', ' ', prop ).strip()
            sinopsis = sinopsisa[:-15]
        if 'Dirección' in typ :
            directors = re.split(',' , re.sub( '\s+', ' ', prop ).strip()) 
        if 'Año' in typ :
            anno = re.sub( '\s+', ' ', prop ).strip()
        if 'País' in typ :
            pais = re.sub( '\s+', ' ', prop ).strip()
    image = movsoup.find('img' , itemprop="image")
    if not (image is None):
        build_method(name, anno, pais, sinopsis, generos, directors, reparto, image['src'])

def build_serie(name, year, pais, sinopsis, generos, directors, reparto, image):
    name = name[:-11]
    already = sess.query(Serie).filter(Serie.title == name)
    if already.count() == 0:
        serie = Serie(title=name , year= int(year), country=pais , sinopsis=sinopsis)
        for g in generos:
            serie.genders.append(SerieGender(name=g))
        for d in directors:
            serie.directors.append(Director(name=d))
        for a in reparto:
            serie.actors.append(Actor(name= a))
        sess.add_all([serie])
        sess.commit()
        #WINDOWS
        #with urllib.request.urlopen(image) as response, open('web\img\Work\Series'+ '\\' + str(serie.id) + 'image.jpeg', 'wb') as out_file:
        #UBUNTU
        with urllib.request.urlopen(image) as response, open('web/img/Work/Series'+ '/' + str(serie.id) + 'image.jpeg', 'wb') as out_file:
            data = response.read()
            out_file.write(data)
    else:
        print('Serie ' + name + ' already exists')
    
def build_movie(name, year, pais, sinopsis, generos, directors, reparto, image):
    already = sess.query(Movie).filter(Movie.title == name)
    if already.count() == 0:
        movie = Movie(title=name , year= int(year), country=pais , sinopsis=sinopsis)
        for g in generos:
            movie.genders.append(MovieGender(name=g))
        for d in directors:
            movie.directors.append(Director(name=d))
        for a in reparto:
            movie.actors.append(Actor(name= a))
        sess.add_all([movie])
        sess.commit()
        #WINDOWS
        #with urllib.request.urlopen(image) as response, open('web\img\Work\Movies'+ '\\' + str(movie.id) + 'image.jpeg', 'wb') as out_file:
        #UBUNTU
        with urllib.request.urlopen(image) as response, open('web/img/Work/Movies'+ '/' + str(movie.id) + 'image.jpeg', 'wb') as out_file:
            data = response.read()
            out_file.write(data)
    else: 
        print("Movie " + name + ' already exists')
        
def search(listdir , stype='' ):
    urlstart = 'https://www.filmaffinity.com/es/advsearch.php?stext='
    urlmid = '&stype%5B%5D=title&country=&genre='
    urlend = '&fromyear=&toyear='
    movies = []
    with open(listdir , "r") as std:
        movies = std.readlines()
    not_found = ''
    direct = ''
    
    for m in movies:
        s = re.sub( ' +', ' ', m ).strip()
        if(stype == ''):
            already = sess.query(OnExistance).filter(OnExistance.name == m, OnExistance.tipo == 'Movie')
        if(stype == 'TV_SE'):
            already = sess.query(OnExistance).filter(OnExistance.name == m, OnExistance.tipo == 'Serie' )
        print(already.count())
        if(already.count() == 0):
            if(stype == ''):
                one = OnExistance(name = m, tipo = 'Movie')
            if(stype == 'TV_SE'):
                one = OnExistance(name = m, tipo = 'Serie' )
            sess.add_all([one])
            sess.commit()
            s = s.replace(' ' , '+')
            url = urlstart + s + urlmid + stype + urlend
            print(url)
            page = urllib.request.urlopen(url).read()
            soup = BeautifulSoup(page)
            soup.prettify()
            i = 0
            anchor = soup.find(class_='mc-title')
            if not (anchor is None):
                a = anchor.a
                print(a['href'])
                if(stype == ''):
                    extract_info(a['href'], build_movie)
                    #WINDOWS
                    #direct = 'web\img\Work\Movies\\notfoundmovies.txt'
                    #UBUNTU
                    direct = 'web/img/Work/Movies/notfoundmovies.txt'
                if(stype == 'TV_SE'):
                    extract_info(a['href'], build_serie)
                    #WINDOWS
                    #direct = 'web\img\Work\Series\\notfoundseries.txt'
                    #UBUNTU
                    direct = 'web/img/Work/Series/notfoundseries.txt'
                i = i + 1
            else: 
                not_found += ( m + '\n' )
        else:
            print('ya has hecho esta busqueda ' + m)
    if(stype == ''):
        #WINDOWS
        #direct = 'web\img\Work\Movies\\notfoundmovies.txt'
        #UBUNTU
        direct = 'web/img/Work/Movies/notfoundmovies.txt'
    if(stype == 'TV_SE'):
        #WINDOWS
        #direct = 'web\img\Work\Series\\notfoundseries.txt'
        #UBUNTU
        direct = 'web/img/Work/Series/notfoundseries.txt'
    print(direct + '**')
    with open(direct , 'at')as std:
                    std.write(not_found)
     

############### WINDOWS ###################
# clean('web/img/Work/Series/series.txt')
# clean('web/img/Work/Movies/movies.txt')
# clean('web/img/Work/Games/games.txt')
# search('web\img\Work\Series\series.txt', 'TV_SE')
# search('web\img\Work\Movies\movies.txt')
# find_games('web\img\Work\Games\games.txt')
###########################################

################ UBUNTU ###################
# clean('web/img/Work/Series/series.txt')
# clean('web/img/Work/Movies/movies.txt')
# clean('games.txt')
# search('series.txt', 'TV_SE')
# search('movies.txt')
find_games('games.txt')
###########################################
sess.close()

