
from DBstructure import *
import DBstructure
from sqlalchemy.orm.exc import NoResultFound
import base64
import shutil

def add_category_to_game(game , category):
    print('QQQQQQQQ')
    print(category)
    cat = find_category(category)
    game.category = cat
    sess.commit()
    print(game.category.name)

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
        print('hser')
        serie = sess.query(Serie).filter(Serie.id == id).one()
        if not delete:
            print('update')
            serie.title = title
            serie.year = year
            serie.pais = pais
            serie.sinopsis = sinopsis
            serie.score = score
            if image != '':
                change_cover(serie, image, series_dir)
        else:
            print('HERE!!')
            remove_images(serie.id, series_dir)
            print('HERE222222!!')
            sess.delete(serie)
            print('Done delete')
        sess.commit()
    else:
        print('Creating serie')
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
        print('done creating')
        sess.commit()
        change_cover(serie, image, series_dir)
        print(serie.title)
        print('Out of here')

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
        Movie = DBstructure.Movie(title=title , year= int(year), country=pais , sinopsis=sinopsis, score=score)
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
    print('Creating')
    print(id)
    if id != -1: 
        game = sess.query(DBstructure.Game).filter(DBstructure.Game.id == id).one()
        if not delete:
            print('here')
            game.name = name
            game.launch = launch
            game.description = description
            game.game_mode = game_mode
            game.language = language
            game.puntuacion = float(puntuacion)
            game.size = size
            print('name:', name)
            print('launch:',launch)
            print('desc:',description)
            print('gm:',game_mode)
            print('lang:',language)
            print('score:',puntuacion)
            print('size:', size)
            # game.max_players = max_players
            # game.min_players = min_players
            if image != '':
                print('here!!!!!!!!!!!!!!!!!!')
                change_cover(game, image, games_dir)
            if len(captures) != 0:
                change_captures(game, captures)
            print('EEEEEEEEEEE', category)
            add_category_to_game(game, category)
            print('out again')
            change_req(game, requirements)
            
        else:
            print('ÉRASEEEEEEE')
            remove_images(game.id, games_dir ,True)
            del_game(game)
        sess.commit()
    else:
        print("heresasssss")
        print('name:', name)
        print('launch:',launch)
        print('desc:',description)
        print('gm:',game_mode)
        print('lang:',language)
        print('score:',puntuacion)
        print('category:', category)
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
    print(gender)
    if not(game is None) and game != -1:
        for g in game.genders:
            if g.name == gender:
                game.genders.remove(g)
                sess.commit()
                break
    print(game.genders)

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

def change_captures(game, images):
    old = game.captures_list
    print(old)
    print()
    c = len(old)
    for o in old:
        if not(o in images):
            os.remove(o)
    for i in images:
        if not(i in old):
            to_write = i[23:]
            with open(games_dir +  slash + str(game.id) + slash +'image' + str(c) +'.jpeg', 'wb') as out_file: 
                data = base64.b64decode(to_write)
                out_file.write(data)
            c +=1 
    print('OUT OF HERE')

def remove_images(id, path, game=False):
    print('removing images')
    print(path + str(id) + 'image.jpeg')
    try:
        os.remove(path + str(id) + 'image.jpeg')
        if game:
            print('got here')
            shutil.rmtree(path + str(id))
    except Exception:
        print(e)
        print('Not found')
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
    print(name)
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
        print(gender)
        print(gender.name)
        tv.genders.append(gender)
        sess.add_all([gender])
        sess.commit()
        print('done add gendrer')
        for g in tv.genders:
            print(g.name)

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
    print('Game leaving')
    for r in game.requirements:
        sess.delete(r)
    sess.delete(game)
    sess.commit()
    print('Game Gone')

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
        print('had to here')
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
