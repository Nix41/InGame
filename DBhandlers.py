
from DBstructure import *
import DBstructure
from sqlalchemy.orm.exc import NoResultFound
import base64
import shutil

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

def CRUD_Serie(title="", year=0, pais="", sinopsis="", generos=[], directors=[], reparto=[],id=-1, image="", delete=False):
    if id != -1: 
        serie = sess.query(Serie).filter(Serie.id == id).one()
        if not delete:
            serie.title = title
            serie.year = year
            serie.pais = pais
            serie.sinopsis = sinopsis
            if image != '':
                change_cover(serie, image, series_dir)
        else:
            remove_images(serie.id, series_dir)
            sess.delete(serie)
        sess.commit()
    else:
        serie = Serie(title=title , year= int(year), country=pais , sinopsis=sinopsis)
        for g in generos:
            add_tv_gender2(serie, g, False)
        for d in directors:
            add_director2(serie, d)
        for a in reparto:
            add_actor2(serie, a)
        sess.add_all([serie])
        sess.commit()
        change_cover(serie, image, series_dir)

def CRUD_Movie(title="", year=0, pais="", sinopsis="", generos=[], directors=[], reparto=[],id=-1, image="", delete=False):
    if id != -1: 
        movie = sess.query(DBstructure.Movie).filter(DBstructure.Movie.id == id).one()
        if not delete:
            movie.title = title
            movie.year = year
            movie.pais = pais
            movie.sinopsis = sinopsis
            if image != '':
                change_cover(movie, image, movies_dir)
        else:
            remove_images(movie.id, movies_dir)
            sess.delete(movie)
        sess.commit()
    else:
        Movie = DBstructure.Movie(title=title , year= int(year), country=pais , sinopsis=sinopsis)
        for g in generos:
            add_tv_gender2(movie, g)
        for d in directors:
            add_director2(movie, d)
        for a in reparto:
            add_actor2(movie, a)
        sess.add_all([movie])
        sess.commit()
        change_cover(movie, image, movies_dir)

def CRUD_Game(name="", description="", game_mode="", language="", launch=0, puntuacion=0, category="", genders=[], requirements=[], id=-1, image="", captures=[], delete=False):
    if id != -1: 
        game = sess.query(DBstructure.Game).filter(DBstructure.Game.id == id).one()
        if not delete:
            game.name = name
            game.launch = launch
            game.description = description
            game.game_mode = game_mode
            game.language = language
            game.puntuancion = puntuacion
            # game.max_players = max_players
            # game.min_players = min_players
            if image != '':
                change_cover(game, image, games_dir)
            if len(captures) != 0:
                load_captures(game.id, captures)
            return game
        else:
            remove_images(game.id, games_dir ,True)
            del_game(game)
        sess.commit()
    else:
        game = DBstructure.Game(name = name, description= description, game_mode =game_mode, language= language, launch= launch, puntuacion = puntuacion )
        for g in genders:
            add_game_gender(game, g)
        for r in requirements[0]:
            add_requirement(game, r['type'], r['req'], True)
        for r in requirements[1]:
            add_requirement(game, r['type'], r['req'], False)    
        add_category_to_game(game, category)
        sess.add_all([game])
        sess.commit()
        change_cover(game, image, games_dir)
        load_captures(game.id, captures)
        return game

def add_game_gender(game, gender):
    try:  
        gend = sess.query(GameGender).filter(GameGender.name == gender).one()
    except NoResultFound:
        gend = GameGender(name = gender)
    game.genders.append(gend)
    sess.commit()

def del_game_gender(game, gender):
    gm = find_game(game)
    if gm != -1:
        for g in gm.genders:
            if g.name == gender:
                gm.genders.remove(g)
                break

def add_requirement(game, type, req, minor):
    reqd = Requirement(req_type = type , req = req)
    gr = GameReq(req = reqd, minormax = minor)
    game.requirements.append(gr)

def change_cover(obj, image, dir_path):
    to_write = image[23:]
    with open(dir_path + str(obj.id) + 'image.jpeg', 'wb') as out_file: 
        data = base64.b64decode(to_write)
        out_file.write(data)

def load_captures(id, images):
    dirt = games_dir + str(id)
    try:
        os.mkdir( dirt)
    except: FileExistsError
    count = 0
    for i in images:
        to_write = i[23:]
        with open(dirt +  slash +'image' + str(count) +'.jpeg', 'wb') as out_file: 
            data = base64.b64decode(to_write)
            out_file.write(data)
        count +=1 

def remove_images(id, path, game=False):
    try:
        os.remove(path + str(id) + 'image.jpeg')
        if game:
            shutil.rmtree(path + str(id))
    except Exception:
        pass
    
def add_director(tv, director, movie=True):
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

def del_director(tv, director, movie=True):
    if movie:
        tvo = find_movie(tv)
    else:
        tvo = find_serie(tv)
    if tvo != -1:
        for d in tvo.directors:
            if d.name == director:
                tvo.directors.remove(d)
    sess.commit()

def add_director2(tv, director):
    try: 
        director = sess.query(Director).filter(Director.name == director).one()
    except NoResultFound:
        director = Director(name = director)
    tv.directors.append(director)
    sess.commit()

def add_actor(tv, actor, movie=True):
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

def del_actor(tv, actor, movie=True):
    if movie:
        tvo = find_movie(tv)
    else:
        tvo = find_serie(tv)
    if tvo != -1:
        for d in tvo.actors:
            if d.name == actor:
                tvo.actors.remove(d)
    sess.commit()

def add_actor2(tv, actor):
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

def add_tv_gender2(tv, name, movie=True):
    if movie:
        try: 
            gender = sess.query(MovieGender).filter(MovieGender.name == name).one()
        except NoResultFound:
            gender = MovieGender(name = name)
    else:
        try: 
            gender = sess.query(SerieGender).filter(SerieGender.name == name).one()
        except NoResultFound:
            gender = SerieGender(name = name)
    tv.genders.append(gender)
    sess.commit()

def del_tv_gender(tv, gender, movie=True):
    if movie:
        tvo = find_movie(tv)
    else:
        tvo = find_serie(tv)
    if tvo != -1:
        for d in tvo.genders:
            if d.name == gender:
                tvo.genders.remove(d)
    sess.commit()

def add_topic(tv, name, movie=True):
    if movie:
        tvo = find_movie(tv)
        table = MovieTopic
    else:
        tvo = find_serie(tv)
        table = SerieTopic
    if tvo != -1:
        try: 
            topic = sess.query(table).filter(table.name == name).one()
        except NoResultFound:
            topic = table(name = name)
        tvo.topics.append(topic)
    sess.commit()

def add_topic2(tv, name, movie=True):
    if movie:
        try: 
            topic = sess.query(MovieTopic).filter(MovieTopic.name == name).one()
        except NoResultFound:
            topic = MovieTopic(name = name)
    else:
        try: 
            topic = sess.query(SerieTopic).filter(SerieTopic.name == name).one()
        except NoResultFound:
            topic = SerieTopic(name = name)
    tv.topics.append(topic)
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

def find_game(ids):
    try: 
        g = sess.query(Game).filter(Game.id == ids).one()
        return g
    except NoResultFound:
        return -1

def del_game(game):
    for r in game.requirements:
        sess.delete(r)
    sess.delete(game)
    sess.commit()

def get_downloads():
    d = {}
    with open(g_list , "r") as std:
        d['games'] = std.read()
    with open(s_list , "r") as std:
        d['series'] = std.read()
    with open(m_list , "r") as std:
        d['movies'] = std.read()
    return d

def set_downloads(games, series, movies):
    with open(g_list , "w") as std:
        std.write(games)
    with open(s_list , "w") as std:
        std.write(series)
    with open(m_list , "w") as std:
        std.write(movies)
        
