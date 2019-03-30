
from DBstructure import *
from utils import clean
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import urllib.request

def get_captures(game, ids):
    i = 0
    #WINDOWS#
    #dirt = 'Work\Games\\' + str(ids)
    #UBUNTU
    dirt = 'Work/Games/' + str(ids)
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
    sep = re.split(': | \(' , req)
    print(sep)
    if len(sep) > 1:
        print('h1')
        reqd = Requirement(req_type = sep[0] , req = sep[1])
    else: 
        print('h2')
        reqd = Requirement(req_type = sep[0] , req = sep[0])

    if boo == 0:
        print('h3')
        gr = GameReq(req = reqd, minormax = False)
    else:
        print('h4')
        gr = GameReq(req = reqd, minormax = True)
    game.requirements.append(gr)
    
def requisitos(url, game):
    req = urllib .request.urlopen(url)
    soup = BeautifulSoup(req)
    soup.prettify()
    regex = re.compile('.*list_foro.*')
    reqs = soup.find_all(class_= regex)
    i = 0
    for gr in reqs:
        print(str(i))
        for lis in gr.find_all('li'):
            print(str(lis.get_text()))
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
                print(resp.get_attribute('href'))
                s = resp.get_attribute('href')
                print('QQ   ', s)
                game = urllib.request.urlopen(s).read()
                soup_game = BeautifulSoup(game)
                soup_game.prettify()
                game_name = soup_game.title.string
                description = "" +soup_game.select_one("#adpepito").get_text()
                jname = game_name[:-18]
                here = sess.query(Game).filter(Game.name == jname)
                p_element = soup_game.find(class_='pr t6')
                if p_element is None:
                    puntuacion = 0
                else:
                    puntuacion_str = re.split(',', soup_game.find(class_='pr t6').get_text())
                    puntuacion = 0
                    for i in range(len(puntuacion_str)):
                        puntuacion += (int)(puntuacion_str[i]) * (10**(-i))
                        print('*********',puntuacion, "***")


                for head in soup_game.find_all('dt'):
                    typ = head.get_text()
                    prop = head.find_next('dd').get_text()
                    if 'Lanzamiento' in typ :
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
                        check1 = re.split(' ', prop)
                        check2 = re.split('-',check1[0])
                        if len(check2) > 1:
                            players = (int)(check2[1])
                        else:
                            players = (int)(check2[0])
                        if '(' in prop:
                            ind = prop.find('(')
                            ind2 = prop.find(')')
                            game_type = prop[ind + 1:ind2]

                    if 'Idioma' in typ:
                        language = prop
                   
                if here.count() == 0:
                    this_game = Game(name = jname, description= description, players =players, game_mode =game_type, language= language, launch= launch, puntuacion = puntuacion )
                    for gender in soup_game.find_all('a', href=True):
                        if 'juegos-generos' in gender['href']:
                            gender_name = gender.get_text()[-8:]
                            qs = sess.query(GameGender).filter(GameGender.name == gender_name)
                            if(qs.count() == 0):
                                this_game.genders.append(GameGender(name= gender_name))
                            else:
                                this_game.genders.append(qs.first())
                    req = gen_requisitos(s)
                    requisitos(req, this_game)  
                    sess.add_all([this_game])
                    sess.commit()
                    get_captures(soup_game , this_game.id)
                    image = soup_game.find(rel='image_src')
                    print('****************')
                    im = image['href']
                    print(im)
 #                   with urllib.request.urlopen(im) as response, open('Work\Games\\' + str(this_game.id) + 'image.jpeg', 'wb') as out_file:
                    with urllib.request.urlopen(im) as response, open('Work/Games/' + str(this_game.id) + 'image.jpeg', 'wb') as out_file: 
                        data = response.read()
                        out_file.write(data)
            except NoSuchElementException:
                not_found += (g + '\n')
                print('it does not exist')
        else:
            print('ya has hecho esta busqueda ' + g)
    #WINDOW
    #with open('Work\Games\\notfound.txt' , 'at') as std:
    #UBUNTU
    with open('Work/Games/notfound.txt' , 'at') as std:
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
        #with urllib.request.urlopen(image) as response, open('Work\Series'+ '\\' + str(serie.id) + 'image.jpeg', 'wb') as out_file:
        #UBUNTU
        with urllib.request.urlopen(image) as response, open('Work/Series'+ '/' + str(serie.id) + 'image.jpeg', 'wb') as out_file:
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
        #with urllib.request.urlopen(image) as response, open('Work\Movies'+ '\\' + str(movie.id) + 'image.jpeg', 'wb') as out_file:
        #UBUNTU
        with urllib.request.urlopen(image) as response, open('Work/Movies'+ '/' + str(movie.id) + 'image.jpeg', 'wb') as out_file:
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
                    #direct = 'Work\Movies\\notfoundmovies.txt'
                    #UBUNTU
                    direct = 'Work/Movies/notfoundmovies.txt'
                if(stype == 'TV_SE'):
                    extract_info(a['href'], build_serie)
                    #WINDOWS
                    #direct = 'Work\Series\\notfoundseries.txt'
                    #UBUNTU
                    direct = 'Work/Series/notfoundseries.txt'
                i = i + 1
            else: 
                not_found += ( m + '\n' )
        else:
            print('ya has hecho esta busqueda ' + m)
    if(stype == ''):
        #WINDOWS
        #direct = 'Work\Movies\\notfoundmovies.txt'
        #UBUNTU
        direct = 'Work/Movies/notfoundmovies.txt'
    if(stype == 'TV_SE'):
        #WINDOWS
        #direct = 'Work\Series\\notfoundseries.txt'
        #UBUNTU
        direct = 'Work/Series/notfoundseries.txt'
    print(direct + '**')
    with open(direct , 'at')as std:
                    std.write(not_found)
 
        
############### WINDOWS ###################
# clean('Work/Series/series.txt')
# clean('Work/Movies/movies.txt')
# clean('Work/Games/games.txt')
# search('Work\Series\series.txt', 'TV_SE')
# search('Work\Movies\movies.txt')
# find_games('Work\Games\games.txt')
###########################################

################ UBUNTU ###################
# clean('Work/Series/series.txt')
# clean('Work/Movies/movies.txt')
# clean('Work/Games/games.txt')
#search('Work/Series/series.txt', 'TV_SE')
#search('Work/Movies/movies.txt')
#find_games('games.txt')
###########################################
sess.close()

