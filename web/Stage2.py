
# coding: utf-8

import urllib.request
import sqlalchemy
from sqlalchemy import create_engine  
from sqlalchemy import Column, String , Integer , Table, ForeignKey, Boolean, DateTime,Float
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy.orm import sessionmaker , relationship, backref, Session
from sqlalchemy.sql import func
from bs4 import BeautifulSoup
import re
import os
import datetime
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException



####### WINDOWS ########
# direct = 'Work\\'
# try:
#     os.mkdir( direct)
# except: FileExistsError
# direct = 'Work\Games\\'
# try:
#     os.mkdir( direct)
# except: FileExistsError
# direct = 'Work\Movies\\'
# try:
#     os.mkdir( direct)
# except: FileExistsError
# direct = 'Work\Series\\'
# try:
#     os.mkdir( direct)
# except: FileExistsError
###########################
######### LINUX ###########
direct = 'Work/'
try:
    os.mkdir( direct)
except: FileExistsError
direct = 'Work/Games/'
try:
    os.mkdir( direct)
except: FileExistsError
direct = 'Work/Movies/'
try:
    os.mkdir( direct)
except: FileExistsError
direct = 'Work/Series/'
try:
    os.mkdir( direct)
except: FileExistsError
##########################

Base = declarative_base()

gamegen_table = Table('gamegen', Base.metadata,
    Column('game_id', Integer, ForeignKey('game.id')),
    Column('gender_id', Integer, ForeignKey('gamegender.id'))
    )

class TimestampMixin(object):
    created_at = Column(DateTime, default=func.now())

class GameGender(Base):
    __tablename__ = 'gamegender'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    games = relationship("Game", secondary=gamegen_table, backref='genders')
    
class GameReq(Base):
    __tablename__ = 'gamereq'
    left_id = Column(Integer, ForeignKey('game.id'), primary_key=True)
    right_id = Column(Integer, ForeignKey('requirement.id'), primary_key=True)
    minormax = Column(Boolean)
    game = relationship("Game", back_populates="requirements")
    req = relationship("Requirement", back_populates="games")

#class Game(TimestampMixin, Base):
class Game(Base):
    __tablename__ = 'game'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    requirements = relationship("GameReq", back_populates="game")
    puntuacion = Column(Float)
    launch = Column(DateTime)
    players = Column(Integer)
    game_mode = Column(String)
    language = Column(String)

class Requirement(Base):
    __tablename__ = 'requirement'
    id = Column(Integer, primary_key=True)
    req_type = Column(String)
    req = Column(String)
    games = relationship("GameReq", back_populates="req")
    
moviedir_table = Table('moviedir', Base.metadata,
    Column('movie_id', Integer, ForeignKey('movie.id')),
    Column('director_id', Integer, ForeignKey('director.id'))
    )
movieactor_table = Table('movieactor', Base.metadata,
    Column('movie_id', Integer, ForeignKey('movie.id')),
    Column('actor_id', Integer, ForeignKey('actor.id'))
    )
moviegen_table = Table('moviegen', Base.metadata,
    Column('movie_id', Integer, ForeignKey('movie.id')),
    Column('moviegender_id', Integer, ForeignKey('moviegender.id'))
    )

seriedir_table = Table('seriedir', Base.metadata,
    Column('serie_id', Integer, ForeignKey('serie.id')),
    Column('director_id', Integer, ForeignKey('director.id'))
    )
serieactor_table = Table('serieactor', Base.metadata,
    Column('serie_id', Integer, ForeignKey('serie.id')),
    Column('actor_id', Integer, ForeignKey('actor.id'))
    )
seriegen_table = Table('seriegen', Base.metadata,
    Column('serie_id', Integer, ForeignKey('serie.id')),
    Column('seriegender_id', Integer, ForeignKey('seriegender.id'))
    )
    
class Director(Base):
    __tablename__ = 'director'
    id= Column(Integer, primary_key= True)
    name = Column(String)
    movies = relationship("Movie", secondary=moviedir_table, backref='directors')
    series = relationship("Serie", secondary=seriedir_table, backref='directors')
    
class Actor(Base):
    __tablename__ = 'actor'
    id= Column(Integer, primary_key= True)
    name = Column(String)
    movies = relationship("Movie", secondary=movieactor_table, backref='actors')
    series = relationship("Serie", secondary=serieactor_table, backref='actors')
    
class MovieGender(Base):
    __tablename__ = 'moviegender'
    id= Column(Integer, primary_key= True)
    name = Column(String)
    movies = relationship("Movie", secondary=moviegen_table, backref='genders')
    
#class Movie(TimestampMixin, Base):
class Movie(Base):
    __tablename__ = 'movie'
    id= Column(Integer, primary_key= True)
    title = Column(String)
    year = Column(Integer)
    country = Column(String)
    sinopsis = Column(String)
    
class SerieGender(Base):
    __tablename__ = 'seriegender'
    id= Column(Integer, primary_key= True)
    name = Column(String)
    series = relationship("Serie", secondary=seriegen_table, backref='genders')

#class Serie(TimestampMixin, Base):    
class Serie(Base):
    __tablename__ = 'serie'
    id= Column(Integer, primary_key= True)
    title = Column(String)
    year = Column(Integer)
    country = Column(String)
    sinopsis = Column(String)

class OnExistance(Base):
    __tablename__ = 'onexistance'
    id= Column(Integer, primary_key= True)
    name = Column(String)
    tipo = Column(String)
    
e = create_engine("sqlite:///yasmany")
Base.metadata.create_all(e)

sess = Session(e)

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

def gen_reuisitos(gameurl):
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
                        months={'enero':1, 'febrero':2, 'marzo':3, 'abril':4, 'mayo':5, 'junio':6, 'julio':7, 'agosto':8, 'septiembre':9, 'octubre':10, 'noviembre':11, 'diciembre':12}
                        if prop in months:
                            month = prop
                        else:
                            month = 'enero'
                        day = (int)(date_str[0])
                        if day > 31:
                            year = day 
                            day = 1
                        else: 
                            year = (int)(date_str[4])
                        launch = datetime.datetime(day=day, month=months[month], year=year)
                        
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
                    req = gen_reuisitos(s)
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
            
def clean_line(A):
    B = ""
    x = 0
    bool = 0
    while 1:
        if x >= len(A):
            break
        if (A[x] == "[") or (A[x] == "(") or (A[x] == "{"):
            bool = 1
        else:
            if (bool == 1) and ((A[x] == "]") or (A[x] == ")") or (A[x] == "}")):
                x += 1
                if (x < len(A) and A[x] != "[") and (A[x] != "(") and (A[x] != "{"):
                    bool = 0
        if bool == 0 and x < len(A):
            B = B + A[x]
        x += 1
    bool = 0
    cnt = 0
    C = ""
    x = len(B) - 1
    if (B[len(B) - 1] == "B") and (B[len(B) - 2] == "M" or B[len(B) - 2] == "G"):
        while 1:
            if x == -1:
                break
            if cnt < 2:
                if B[x] == " ":
                    cnt += 1
            else:
                C = B[x] + C
            x -= 1
    else:
        C = B
    print(C)
    return C

def stupidshit(w, p):
    new = ''
    for i in range(p):
        new += w[i]
    for i in range(p+1,len(w)):
        new += w[i]
    return new

def clean(path):
    with open(path , "r") as std:
        movies = std.readlines()
    new = []

    for m in movies:
        s = re.sub( ' +', ' ', m ).strip()
        if(len(s) > 1):
            t = clean_line(s)
            new.append(t + '\n')
    with open(path, 'w') as std:
        std.writelines(new)
        
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
find_games('games.txt')
###########################################
sess.close()
 
############ FILTERS ######################
###########################################

def get_game_genders():
    genders = []
    for gen in sess.query(GameGender).all():
        genders.append(gen.name)
    #print('genders: ',len(genders))
    return genders

def get_serie_genders():
    genders = []
    for gen in sess.query(SerieGender).all():
        genders.append(gen.name)
    return genders

def get_movie_genders():
    genders = []
    for gen in sess.query(MovieGender).all():
        genders.append(gen.name)
    return genders

def filter_games(name = "", gender = "" ):
    games = {}
    for c in sess.query(Game).filter(Game.name.contains(name)):
        genders = []
        print()
        print( c.launch )
        print(c.players)
        print(c.game_mode)
        print(c.language)
        print(c.puntuacion)
        print(c.name)
        print()
        gender_filter = False
        # for g in c.genders:
        #     if g.name.contains(gender):
        #         gender_filter = True
        #     genders.append(g.name)
        # requirements = []
        # requirements.append([])
        # requirements.append([])
        # for r in c.requirements:
        #     req = {}
        #     req['type'] = r.req.req_type
        #     req['req'] = r.req.req
        #     if r.minormax == True:
        #         requirements[0].append(req)
        #     else:
        #         requirements[1].append(req)
        # if gender_filter:
        #     games[c.id] = {}
        #     games[c.id]['id'] = c.id
        #     games[c.id]['name'] = c.name
        #     games[c.id]['description'] = c.description
        #     games[c.id]['genders'] = genders
        #     games[c.id]['requirements'] = requirements
    return games

def filter_series(name = "", gender="", actor="", director=""):
    series = {}
    for s in sess.query(Serie).filter(Serie.title.contains(name)):
        genders = []
        gender_filter = False
        for g in s.genders:
            if g.name.contains(gender):
                gender_filter = True
            genders.append(g.name)
        actor_filter  = False
        actors = []
        for a in s.actors:
            if a.name.conatains(actor):
                actor_filter = True
            actors.append(a.name)
        director_filter = False
        directors = []
        for d in s.directors:
            if d.name.conatains(director):
                director_filter = True
            directors.append(d.name)
        if gender_filter and actor_filter and director_filter:
            series[s.id] = {}
            series[s.id]['id'] = s.id
            series[s.id]['title'] = s.title
            series[s.id]['year'] = s.year 
            series[s.id]['country'] = s.sinopsis
            series[s.id]['genders'] = genders
            series[s.id]['actors'] = actors
            series[s.id]['directors'] = directors
    return series

def filter_movies(name = "", gender="", actor="", director=""):
    movies = {}
    for c in sess.query(Movie).filter(Movie.title.contains(name)):
        genders = []
        gender_filter = False
        for g in c.genders:
            if g.name.contains(gender):
                gender_filter = True
            genders.append(g.name)
        actor_filter = False
        actors = []
        for a in c.actors:
            if a.name.contains(actor):
                actor_filter = True
            actors.append(a.name)
        directors = []
        director_filter = False
        for d in c.directors:
            if d.name.contains(director):
                director_filter = True
            directors.append(d.name)
        if gender_filter and actor_filter and director_filter:
            movies[c.id] = {}
            movies[c.id]['id'] = c.id
            movies[c.id]['title'] = c.title
            movies[c.id]['year'] = c.year 
            movies[c.id]['country'] = c.sinopsis
            movies[c.id]['genders'] = genders
            movies[c.id]['actors'] = actors
            movies[c.id]['directors'] = directors
    return movies

### RECUERDA AGREGAR CREATED_AT ANTES DE TESTEAR##
def get_recent():
    recent = []
    # games = sess.query(Game).order_by(Game.created_at)[-3:]
    # series = sess.query(Serie).order_by(Serie.creates_at)[-3:]
    # movies = sess.query(Movie).order_by(Movie.created_at)[-3:]
    games = sess.query(Game).order_by(Game.id)[-3:]
    series = sess.query(Serie).order_by(Serie.id)[-3:]
    movies = sess.query(Movie).order_by(Movie.id)[-3:]
    for i in range(3):
        game = {}
        game['id'] = games[i].id
        game['name'] = games[i].name
        game['description'] = games[i].description
        serie = {}
        serie['id'] = series[i].id
        serie['name'] = series[i].title
        serie['description'] = series[i].sinopsis
        movie = {}
        movie['id'] = movies[i].id
        movie['name'] = movies[i].title
        movie['description'] = movies[i].sinopsis
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


filter_games()