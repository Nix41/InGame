
from DBstructure import *
from DBhandlers import *
from utils import clean, make_lists
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import urllib.request
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
import unicodedata
from datetime import datetime
from socket import timeout

digits = ['1','2','3','4', '5','6','7','8','9','0']

def get_captures(game, ids):
    print('    Descargando Capturas')
    i = 0
    dirt = games_dir + str(ids)
    try:
        os.mkdir( dirt)
    except: FileExistsError
        
    for im in game.findAll('img', class_='wi100'):
        if not('video' in im['data-src']):
            with urllib.request.urlopen(im['data-src']) as response, open(dirt + slash + 'image' + str(datetime.now()).replace(':','') + '.jpeg', 'wb') as out_file:
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
    space_key = ['Almacenamiento', 'Disco', 'Duro', 'Espacio', 'almacenamiento', 'disco', 'duro', 'espacio']
    sep = re.split(': | \(' , req)
    print('      ',sep)
    if len(sep) > 1:
        reqd = Requirement(req_type = sep[0] , req = sep[1])
    else: 
        reqd = Requirement(req_type = "" , req = sep[0])
    gr = GameReq(req = reqd, minormax = boo)
    (sep[0])
    for key in space_key:
        if key in sep[0]:
            size = 0
            p = re.compile(r'\d+')
            if len(sep) > 1:
                st = p.findall(sep[1])
                if len(st) > 0:
                    size = st[0]
            game.size = size
            break
    game.requirements.append(gr)
    
def requisitos(url, game):
    (url)
    req = urllib .request.urlopen(url)
    soup = BeautifulSoup(req)
    soup.prettify()
    first = True
    category = None
    for gender in soup.find_all('a', href=re.compile('.*juegos-generos.*')):
        gender_name = gender.get_text()
        if not('juego' in gender_name):
            if first:
                first = False
                category = find_category(gender_name)
                game.category = category
            else:
                add_gender_to_game(game, gender_name, category)
    regex = re.compile('.*list_foro.*')
    reqs = soup.find_all(class_= regex)
    i = 0
    for gr in reqs:
        (gr.find_previous().get_text())
        if 'recomendados' in gr.find_previous().get_text():
            print('    Requisitos Recomendados')
            boo = False
        else:
            boo = True
            print('    Requisitos Minimos')
        for lis in gr.find_all('li'):
            extract_req(lis.get_text(), game, boo)
        i = i + 1
    
    ('next')

def find_games(sourcelist):
    urlstart = 'https://www.3djuegos.com/?q='
    urlend = '&zona=resultados-buscador&id_foro=0&subzona=juegos&id_plat=1'
    games = []
    not_found = ''  
    line = None
    with open(sourcelist , "r") as std:
        while (line is None) or line != '':
            try:
                line = std.readline()
                games.append(line)
            except:
                pass
    print('Searching ', len(games), ' Games')
    options = Options()
    options.headless = True
    options.add_argument('--ignore-certificate-errors')
    chrome_prefs = {}
    options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}
    driver = webdriver.Chrome("driver/chromedriver.exe", options=options)
    driver.set_page_load_timeout(60)
    found = []
    for g in games:
        print(g, '   ->  ', type(g))
        s = re.sub( ' +', ' ', g ).strip()
        print('Buscando Juego: ', g[:-1])
        already = sess.query(Game).filter(Game.name == g)
        if already.count() == 0:
            s = s.replace(' ' , '+')
            url = urlstart + s + urlend
            print('url:',url)
            try: 
                driver.get(url)
                resp = driver.find_element_by_xpath('//*[@class="xXx b"]')
                s = resp.get_attribute('href')
                game = urllib.request.urlopen(s).read()
                soup_game = BeautifulSoup(game)
                soup_game.prettify()
                game_name = soup_game.title.string
                description = "" +soup_game.select_one("#adpepito").get_text()
                jname = game_name[:-18]
                print('    Encontrado: ', jname)
                here = sess.query(Game).filter(Game.name == jname)
                p_element = soup_game.find(class_='pr t6')
                if p_element is None:
                    puntuacion = 0
                else:
                    puntuacion_str = re.split(',', soup_game.find(class_='pr t6').get_text())
                    puntuacion = 0
                    for i in range(len(puntuacion_str)):
                        puntuacion += (int)(puntuacion_str[i]) * (10**(-i))
                print('    Score:', puntuacion)
                language=""
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
                        print('    Year:', launch)                    
                    if 'Jugadores' in typ:
                        game_type = prop
                        print('    Game Mode:' , game_type)
                    if 'Idioma' in typ:
                        language = prop 
                        print('    Language:', language)                 
                if here.count() == 0:
                    this_game = Game(name = g[:-1], description= description, game_mode =game_type, language= language, launch= launch, puntuacion = puntuacion )  
                    r = soup_game.find('a' , text='Requisitos')
                    req = r['href']
                    requisitos(req, this_game)
                    get_captures(soup_game , this_game.id)
                    image = soup_game.find(rel='image_src')
                    im = image['href']
                    with urllib.request.urlopen(im) as response, open(games_dir + str(this_game.id) + slash + 'cover' + str(datetime.now()).replace(':','') + '.jpeg', 'wb+') as out_file: 
                        data = response.read()
                        out_file.write(data)
                    one = OnExistance(name = g, tipo = 'Game')  
                    sess.add_all([this_game, one])
                    sess.commit()
                    print('    El juego ha sido descargado Exitosamente')
                    found.append(g)
                else:
                    print('Este juego ya existe')
                    found.append(g)
                    make_lists(g_list, found , 'lists/not_found_games.txt', not_found)
            except TimeoutException:
                not_found = g  
                make_lists(g_list, found , 'lists/not_found_games.txt', not_found)
                not_found = ''
                print('    La pagina se demoro demasiado on ', g)
            except NoSuchElementException:
                not_found = g 
                make_lists(g_list, found , 'lists/not_found_games.txt', not_found)
                not_found = ''
                print('    No se ha podido encontrar el juego', g ,' en la Pagina') 
        else:
            print('    Ya has hecho esta busqueda: ' + g)
            found.append(g)
            make_lists(g_list, found , 'lists/not_found_games.txt', not_found)

    print('Done Download')
    driver.quit()
    

def extract_info(url, build_method, dname):
    url = 'https://www.filmaffinity.com' + url
    mov = urllib.request.urlopen(url)
    movsoup = BeautifulSoup(mov)
    movsoup.prettify()
    info = movsoup.find(class_='movie-info')
    name = ''
    generos = []
    topics = []
    reparto = []
    directors = []
    sinopsis = ''
    anno = ''
    pais = ''
    for head in info.find_all('dt'):
        typ = head.get_text()
        nextI = head.find_next('dd')
        prop = nextI.get_text()
        if 'Título original' in typ :
            name = re.sub( '\s+', ' ', prop ).strip()
            print('    Titulo:', name)
        if 'Género' in typ :
            gens = nextI.find_all('a')
            for g in gens:
                if 'moviegenre' in g['href']:
                    generos.append(g.get_text())
                    print('    Genero ->', g.get_text())
                elif 'movietopic' in g['href']:
                    topics.append(g.get_text())
                    print('    Tema ->', g.get_text())
        if 'Reparto' in typ :
            reparto = re.split(',' , re.sub( '\s+', ' ', prop ).strip())
        if 'Sinopsis' in typ :
            sinopsisa = re.sub( '\s+', ' ', prop ).strip()
            sinopsis = sinopsisa[:-15]
            print('    Sinopsis: ', sinopsis)
        if 'Dirección' in typ :
            directors = re.split(',' , re.sub( '\s+', ' ', prop ).strip()) 
        if 'Año' in typ :
            anno = re.sub( '\s+', ' ', prop ).strip()
            print('    Año: ', anno)
        if 'País' in typ :
            pais = re.sub( '\s+', ' ', prop ).strip()
            print('    País:', pais)
    image = movsoup.find('img' , itemprop="image")
    scor = movsoup.find('div', id="movie-rat-avg")
    try:
        score = float(scor['content'])
    except Exception:
        score = 0
    print('    Score:', score)
    if not (image is None):
        build_method(dname, anno, pais, sinopsis, generos, directors, reparto, image['src'], score, topics)

def build_serie(name, year, pais, sinopsis, generos, directors, reparto, image, score, topics):
    name = name[:-11]
    already = sess.query(Serie).filter(Serie.title == name)
    if already.count() == 0:
        serie = Serie(title=name , year= int(year), country=pais , sinopsis=sinopsis, score=score)
        for g in generos:
            (g)
            add_tv_gender2(serie, g, False)
        print('    Directores:')
        for d in directors:
            print('      -',d)
            add_director2(serie, d)
        print('    Reparto:')
        for a in reparto:
            print('      -',a)
            add_actor2(serie, a)
        for t in topics:
            (t)
            add_topic2(serie, t, False)
        sess.add_all([serie])
        sess.commit()
        try:
            os.mkdir( series_dir + str(serie.id) + slash)
        except: FileExistsError
        with urllib.request.urlopen(image) as response, open(series_dir + str(serie.id) + slash + 'cover'+ str(datetime.now()).replace(':','') +'.jpeg', 'wb') as out_file:
            data = response.read()
            out_file.write(data)
        print('    La serie ha sido descargada exitosamente')
    else:
        print('    La serie ' + name + ' ya exitia')
    
def build_movie(name, year, pais, sinopsis, generos, directors, reparto, image, score, topics):
    already = sess.query(Movie).filter(Movie.title == name)
    if already.count() == 0:
        movie = Movie(title=name , year= int(year), country=pais , sinopsis=sinopsis, score=score)
        for g in generos:
            add_tv_gender2(movie, g)
        print('    Directores:')
        for d in directors:
            print('      -',d)
            add_director2(movie, d)
        print('    Reparto:')
        for a in reparto:
            print('      -',a)
            add_actor2(movie, a)
        for t in topics:
            add_topic2(movie, t)
        sess.add_all([movie])
        sess.commit()
        try:
            os.mkdir( movies_dir + str(movie.id) + slash)
        except: FileExistsError
        with urllib.request.urlopen(image) as response, open(movies_dir+ '/' + str(movie.id) + slash + 'cover'+ str(datetime.now()).replace(':','') +'.jpeg', 'wb') as out_file:
            data = response.read()
            out_file.write(data)
        print('    La pelicula ha sido descargada exitosamente')
    else: 
        ("    La pelicula " + name + ' ya existia')
        
def search(listdir , stype='' ):
    urlstart = 'https://www.filmaffinity.com/es/advsearch.php?stext='
    urlmid = '&stype%5B%5D=title&country=&genre='
    urlend = '&fromyear=&toyear='
    movies = []
    line = None
    with open(listdir , "r") as std:
        while (line is None) or line != '':
            try:
                line = std.readline()
                movies.append(line)
            except:
                pass
    not_found = ''
    direct = ''
    found = []
    for m in movies:
        s = re.sub( ' +', ' ', m ).strip()
        if(stype == ''):
            already = sess.query(Movie).filter(Movie.title == m)
            ('Buscando Pelicula: ', m[:-1])
        if(stype == 'TV_SE'):
            already = sess.query(Serie).filter(Serie.title == m)
            ('Buscando Serie: ', m[:-1])
        if(already.count() == 0):
            s = s.replace(' ' , '+')
            url = urlstart + s + urlmid + stype + urlend
            try:
                page = urllib.request.urlopen(url, timeout=60).read()
            except (urllib.error.HTTPError, urllib.error.URLError, timeout):
                print('La pagina tardo demasiado')
            soup = BeautifulSoup(page)
            soup.prettify()
            i = 0
            anchor = soup.find(class_='mc-title')
            if not (anchor is None):
                a = anchor.a
                ('url:',a['href'])
                if(stype == ''):
                    extract_info(a['href'], build_movie, m[:-1])
                    found.append(m)
                    make_lists(m_list, found , 'lists/not_found_movies.txt', not_found)
                    one = OnExistance(name = m, tipo = 'Movie')
                    sess.add_all([one])
                    sess.commit()
                if(stype == 'TV_SE'):
                    extract_info(a['href'], build_serie, m[:-1])
                    found.append(m)
                    make_lists(s_list, found , 'lists/not_found_series.txt', not_found)
                    one = OnExistance(name = m, tipo = 'Serie' )
                    sess.add_all([one])
                    sess.commit()
                i = i + 1
            else: 
                not_found = ( m )
                if(stype == ''):
                    make_lists(m_list, found , 'lists/not_found_movies.txt', not_found)
                if(stype == 'TV_SE'):
                    make_lists(s_list, found , 'lists/not_found_series.txt', not_found)
                not_found = ''
        else:
            print('    Ya has hecho esta busqueda ' + m)
    print('Done Download')
     
def Down_Games():
    clean(g_list)
    find_games(g_list)
def Down_Series():
    clean(s_list)
    search(s_list, 'TV_SE')
def Down_Movies():
    clean(m_list)
    search(m_list)

# Down_Games()
# Down_Series()
# Down_Movies()

sess.close()



