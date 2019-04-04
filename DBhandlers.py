
from DBstructure import *
from sqlalchemy.orm.exc import NoResultFound

def add_category_to_game(game , category):
    cat = find_category(category)
    game.category = cat

def add_gender_to_game(game, gender, category = None):
    try: 
        gen = sess.query(GameGender).filter(GameGender.name == gender).one()
    except NoResultFound:
        gen = GameGender(name = gender)
    if not(category is None):
        gen.category = category
    game.genders.append(gen)

def find_category(category):
    try: 
        cat = sess.query(GameCategory).filter(GameCategory.name == category).one()
    except NoResultFound:
        cat = GameCategory(name = category)
    return cat

def CRU_Serie(title, year, pais, sinopsis, generos=[], directors=[], reparto=[],id=-1, image_path=""):
    try: 
        serie = sess.query(Serie).filter(Serie.id == id).one()
        serie.title = title
        serie.year = year
        serie.pais = pais
        serie.sinopsis = sinopsis
        for g in generos:
            if not(g in serie.genders):
                add_tv_gender(serie, g)
        # for g in serie.genders:
        #     if not(g in generos):

        for d in directors:
            if not(d in serie.directos):
                add_director(serie, d)
        for a in reparto:
            if not(a in serie.actors):
                add_actor(serie, a)
        sess.commit()
    except NoResultFound:
        serie = Serie(title=title , year= int(year), country=pais , sinopsis=sinopsis)
        for g in generos:
            serie.genders.append(SerieGender(name=g))
        for d in directors:
            serie.directors.append(Director(name=d))
        for a in reparto:
            serie.actors.append(Actor(name= a))
        sess.add_all([serie])
        sess.commit()

def add_director2(tv, director, movie=True):
    if movie:
        tvo = find_movie(tv)
    else:
        tvo = find_serie(tv)
    if tvo != -1:
        try: 
            director = sess.query(Director).filter(Director.name == director).one()
        except NoResultFound:
            director = Director(name = director)
        tvo.directors.append(director)
    sess.commit()

def add_director(tv, director):
    try: 
        director = sess.query(Director).filter(Director.name == director).one()
    except NoResultFound:
        director = Director(name = director)
    tv.directors.append(director)
    sess.commit()

def add_actor2(tv, actor, movie=True):
    if movie:
        tvo = find_movie(tv)
    else:
        tvo = find_serie(tv)
    if tvo != -1:
        try: 
            actor = sess.query(Actor).filter(Actor.name == actor).one()
        except NoResultFound:
            actor = Actor(name = actor)
        tvo.actors.append(actor)
    sess.commit()

def add_actor(tv, actor):
    try: 
        actor = sess.query(Actor).filter(Actor.name == actor).one()
    except NoResultFound:
        actor = Actor(name = actor)
    tv.actors.append(actor)
    sess.commit()

def add_tv_gender(tv, name, movie=True):
    if movie:
        tvo = find_movie(tv)
        table = MovieGender
    else:
        tvo = find_serie(tv)
        table = SerieGender
    if tvo != -1:
        try: 
            gender = sess.query(table).filter(table.name == name).one()
        except NoResultFound:
            gender = table(name = name)
        tvo.genders.append(gender)
    sess.commit()

def find_serie(id):
    try: 
        return sess.query(Serie).filter(Serie.id == id).one()
    except NoResultFound:
        return -1

def find_movie(id):
    try: 
        return sess.query(Movie).filter(Movie.id == id).one()
    except NoResultFound:
        return -1

def find_game(id):
    try: 
        return sess.query(Game).filter(Game.id == id).one()
    except NoResultFound:
        return -1
