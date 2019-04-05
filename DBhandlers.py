
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

def CRUD_Serie(title, year, pais, sinopsis, generos=[], directors=[], reparto=[],id=-1, image_path="", delete=False):
    if id != -1: 
        serie = sess.query(Serie).filter(Serie.id == id).one()
        if not delete:
            serie.title = title
            serie.year = year
            serie.pais = pais
            serie.sinopsis = sinopsis
        else:
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

def CRUD_Movie(title, year, pais, sinopsis, generos=[], directors=[], reparto=[],id=-1, image_path="", delete=False):
    if id != -1: 
        movie = sess.query(Movie).filter(Movie.id == id).one()
        if not delete:
            movie.title = title
            movie.year = year
            movie.pais = pais
            movie.sinopsis = sinopsis
        else:
            sess.delete(movie)
        sess.commit()
    else:
        Movie = Movie(title=title , year= int(year), country=pais , sinopsis=sinopsis)
        for g in generos:
            add_tv_gender2(movie, g)
        for d in directors:
            add_director2(movie, d)
        for a in reparto:
            add_actor2(movie, a)
        sess.add_all([movie])
        sess.commit()

def CRUD_Game(name, description, game_mode, language, launch, puntuacion, category, genders=[], requirements=[], id=-1, image_path="", captures=[], delete=False):
    if id != -1: 
        game = sess.query(Game).filter(Game.id == id).one()
        if not delete:
            game.name = name
            game.launch = launch
            game.description = description
            game.game_mode = game_mode
            game.language = language
            game.puntuancion = puntuacion
            # game.max_players = max_players
            # game.min_players = min_players
            if game.cover_path != image_path and image_path != "":
                change_cover(game, image_path)
        else:
            sess.delete(game)
        sess.commit()
    else:
        Game = Game(name = name, description= description, game_mode =game_mode, language= language, launch= launch, puntuacion = puntuacion )
        for g in genders:
            add_game_gender(game, g)
        for r in requirements[0]:
            add_requirement(game, r['type'], r['req'], True)
        for r in requirements[1]:
            add_requirement(game, r['type'], r['req'], False)
        add_category_to_game(game, category)
        sess.add_all([game])
        sess.commit()

def add_game_gender(game, gender):
    gm = find_game(game)
    if gm != -1:
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

def change_cover(obj, path):
    with open(path, 'rb') as response, open(games_dir + str(obj.id) + 'image.jpeg', 'wb') as out_file: 
        data = response.read()
        out_file.write(data)

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

def find_game(id):
    try: 
        return sess.query(Game).filter(Game.id == id).one()
    except NoResultFound:
        return -1
