
from DBstructure import *
import DBstructure
from sqlalchemy.orm.exc import NoResultFound
import base64
import shutil
from datetime import datetime

def add_category_to_game(game , category):
    #'QQQQQQQQ')
    #category)
    cat = find_category(category)
    game.category = cat
    sess.commit()
    #game.category.name)

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

def CRUD_Serie(title="", year=0, pais="", sinopsis="", generos=[], directors=[], reparto=[],score=0 ,id=-1, image="", topics=[],delete=False):
    if id != -1: 
        #'hser')
        serie = sess.query(Serie).filter(Serie.id == id).one()
        if not delete:
            #'update')
            serie.title = title
            serie.year = year
            serie.pais = pais
            serie.sinopsis = sinopsis
            serie.score = score
            if image != '':
                change_cover(serie, image, series_dir)
        else:
            #'HERE!!')
            remove_images(serie.id, series_dir)
            #'HERE222222!!')
            sess.delete(serie)
            #'Done delete')
        sess.commit()
    else:
        #'Creating serie')
        serie = Serie(title=title , year= int(year), country=pais , sinopsis=sinopsis, score=score)
        for g in generos:
            add_tv_gender2(serie, g, False)
        for d in directors:
            add_director2(serie, d)
        for a in reparto:
            add_actor2(serie, a)
        for t in topics:
            add_topic2(serie, t, False)
        sess.add_all([serie])
        #'done creating')
        sess.commit()
        change_cover(serie, image, series_dir)
        #serie.title)
        #'Out of here')

def CRUD_Movie(title="", year=0, pais="", sinopsis="", generos=[], directors=[], reparto=[],score=0, id=-1, image="", topics=[], delete=False):
    if id != -1: 
        movie = sess.query(DBstructure.Movie).filter(DBstructure.Movie.id == id).one()
        if not delete:
            movie.title = title
            movie.year = year
            movie.pais = pais
            movie.sinopsis = sinopsis
            movie.score = score
            if image != '':
                change_cover(movie, image, movies_dir)
        else:
            remove_images(movie.id, movies_dir)
            sess.delete(movie)
        sess.commit()
    else:
        movie = DBstructure.Movie(title=title , year= int(year), country=pais , sinopsis=sinopsis, score=score)
        for g in generos:
            add_tv_gender2(movie, g)
        for d in directors:
            add_director2(movie, d)
        for a in reparto:
            add_actor2(movie, a)
        for t in topics:
            add_topic2(movie, t)
        sess.add_all([movie])
        sess.commit()
        change_cover(movie, image, movies_dir)
 
def CRUD_Game(name="", description="", game_mode="", language="", launch=0, puntuacion=0, category="", genders=[], requirements=[[],[]], id=-1, image="", captures=[], size=0,delete=False):
    #id)
    if id != -1: 
        game = sess.query(DBstructure.Game).filter(DBstructure.Game.id == id).one()
        if not delete:
            game.name = name
            game.launch = launch
            game.description = description
            game.game_mode = game_mode
            game.language = language
            game.puntuacion = float(puntuacion)
            game.size = size
            if image != '':
                change_cover(game, image, games_dir)
            if len(captures) != 0:
                change_captures(game, captures)
            add_category_to_game(game, category)
            change_req(game, requirements)
            
        else:
            remove_images(game.id, games_dir ,True)
            del_game(game)
        sess.commit()
    else:
        game = DBstructure.Game(name = name, description= description, game_mode =game_mode, language= language, launch= launch, puntuacion = puntuacion, size=size )
        for g in genders:
            add_game_gender(game, g)
        if len(requirements[0]) == 0:
            add_requirement(game, ' ', 'Desconocidos', True)
        if len(requirements[0]) == 0:
            add_requirement(game, ' ', 'Desconocidos', False)
        for r in requirements[0]:
            add_requirement(game, r[0], r[1], True)
        for r in requirements[1]:
            add_requirement(game, r[0], r[1], False)    
        add_category_to_game(game, category)
        sess.add_all([game])
        sess.commit()
        change_cover(game, image, games_dir)
        load_captures(game.id, captures)
        return game

def add_game_gender(game, gender):
    if not(game is None) and game != -1:
        try:  
            gend = sess.query(GameGender).filter(GameGender.name == gender).one()
        except NoResultFound:
            gend = GameGender(name = gender)
        game.genders.append(gend)
        sess.commit()

def del_game_gender(game, gender):
    if not(game is None) and game != -1:
        for g in game.genders:
            if g.name == gender:
                game.genders.remove(g)
                sess.commit()
                break

def add_requirement(game, type, req, minor):
    reqd = Requirement(req_type = type , req = req)
    gr = GameReq(req = reqd, minormax = minor)
    game.requirements.append(gr)

def change_cover(obj, image, dir_path):
    bind, iformat = image_data(image)
    to_write = image[bind:]
    print('Bind:', image)
    try:
        os.mkdir( dir_path + str(obj.id) + slash)
    except: FileExistsError
    try:
        for r, d, f in os.walk(dir_path + str(obj.id) + slash):
            for file in f:
                file = os.path.join(r, file)
                if 'cover' in file:
                    os.remove(file)
    except: Exception
    try:
        with open(dir_path + str(obj.id) + slash + 'cover' + str(datetime.now()).replace(':','') + '.' + iformat, 'wb+') as out_file: 
            data = base64.b64decode(to_write)
            out_file.write(data)
    except:
        print('La imagen tiene problemas, Modifique el juego y cambie la imagen')

def load_captures(id, images):
    dirt = games_dir + str(id)
    print('ID:', id)
    print(dirt)
    try:
        os.mkdir( dirt)
    except: FileExistsError
    count = 0
    for i in images:
        bind, iformat = image_data(i)
        to_write = i[bind:]
        print('loading:', iformat)
        try:
            with open(dirt +  slash +'image' + str(datetime.now()).replace(':','') +'.' + iformat, 'wb') as out_file: 
                data = base64.b64decode(to_write)
                out_file.write(data)
        except:
            print('The image is corrupted')
        count +=1 

def change_captures(game, images):
    old = game.captures_list
    c = len(old)
    for o in old:
        if not(o in images):
            os.remove(o)
    for i in images:
        if not(i in old):
            try:
                bind, iformat = image_data(i)
                to_write = i[bind:]
                with open(games_dir +  slash + str(game.id) + slash +'image' + str(datetime.now()).replace(':','') +'.' + iformat, 'wb') as out_file: 
                    data = base64.b64decode(to_write)
                    out_file.write(data)
                c +=1 
            except Exception:
                print('la imagen tiene problemas')
    #'OUT OF HERE')

def remove_images(id, path, game=False):
    try:
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

def del_director(tv, director):
    if not(tv is None) and tv != -1:
        for d in tv.directors:
            if d.name == director:
                tv.directors.remove(d)
        sess.commit()

def add_director2(tv, director):
    if not(tv is None) and tv != -1:
        try: 
            director = sess.query(Director).filter(Director.name == director).one()
        except NoResultFound:
            director = Director(name = director)
        tv.directors.append(director)
        sess.commit()

def del_actor(tv, actor):
    if not(tv is None) and tv != -1:
        for d in tv.actors:
            if d.name == actor:
                tv.actors.remove(d)
    sess.commit()

def add_actor2(tv, actor):
    if not(tv is None) and tv != -1:
        try: 
            actor = sess.query(Actor).filter(Actor.name == actor).one()
        except NoResultFound:
            actor = Actor(name = actor)
        tv.actors.append(actor)
        sess.commit()

def add_tv_gender2(tv, name, movie=True):
    if not(tv is None) and tv != -1:
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
        sess.add_all([gender])
        sess.commit()

def del_tv_gender(tv, gender):
    if not(tv is None) and tv != -1:
        for d in tv.genders:
            if d.name == gender:
                tv.genders.remove(d)
    sess.commit()

def add_topic2(tv, name, movie=True):
    if not(tv is None) and tv != -1:
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
        sess.add_all([topic])
        sess.commit()

def del_topic(tv, name): 
    if not(tv is None) and tv != -1:
        for t in tv.topics:
            if t.name == name:
                tv.topics.remove(t)
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
    #'Game leaving')
    for r in game.requirements:
        sess.delete(r)
    sess.delete(game)
    sess.commit()
    #'Game Gone')

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

def change_req(game,reqs):
    if len(reqs) == 0:
        #'had to here')
        reqs = [[],[]]
    for r in game.requirements:
        if r.minormax:
            for rq in reqs[0]:
                if rq['type'] == r.req.req_type:
                    r.req.req = rq['req']
        else:
            for rq in reqs[1]:
                if rq['type'] == r.req.req_type:
                    r.req.req = rq['req']
    sess.commit()

def get_counters():
    counters = []
    gc = len(sess.query(Game).all())
    sc = len(sess.query(Serie).all())
    mc = len(sess.query(Movie).all())
    counters.append(gc)
    counters.append(sc)
    counters.append(mc)
    return counters

def image_data(data):
    iformat = ''
    bind = 0
    slash = False
    for s in data:
        if s == ';':
            slash = False
        if slash:
            iformat += s
        if s == '/':
            slash = True
        if s == ',':
            bind += 1
            break
        bind += 1
    print('format:', iformat,'  Point:', bind)
    return bind , iformat
