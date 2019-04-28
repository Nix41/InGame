from DBstructure import *

def Add_Game(Id):
    Id = str(Id)
    game = sess.query(Game).get(Id)
    with open('++Carrito Juegos Ingame.txt', 'a+') as std:
        std.write('[' +str(Id) + '] ' + game.name + '\n')

def Add_Serie(Id):
    Id = str(Id)
    serie = sess.query(Serie).get(Id)
    with open('++Carrito Series Ingame.txt', 'a+') as std:
        std.write('['+ str(Id) + '] ' + serie.title+ '\n')

def Add_Movie(Id):
    Id = str(Id)
    movie = sess.query(Movie).get(Id)
    with open('++Carrito Movies Ingame.txt', 'a+') as std:
        std.write('['+  str(Id) + '] ' + movie.title+ '\n') 
    
def get_games_cart():
    gids = []
    with open('++Carrito Juegos Ingame.txt', 'r+') as std:
        txt = std.readlines()
    for t in txt:
        gids.append(get_id(t))
    games = []
    for i in gids:
        c = sess.query(Game).get(i)
        genders = []
        for g in c.genders:
            genders.append(g.name)
        requirements = []
        requirements.append([])
        requirements.append([])
        for r in c.requirements:
            req = {}
            req['type'] = r.req.req_type
            req['req'] = r.req.req
            if r.minormax == True:
                requirements[0].append(req)
            else:
                requirements[1].append(req)
        game = {}
        game['id'] = c.id
        game['name'] = c.name
        game['description'] = c.description
        game['genders'] = genders
        game['requirements'] = requirements
        game['size'] = c.size
        if not (c.category is None):
            cate = c.category.name
        else:
            cate = ''
        game['category'] = cate
        game['launch'] = c.launch
        game['game_mode'] = c.game_mode
        game['language'] = c.language
        game['score'] = c.puntuacion
        game['cover_path'] = c.cover_path
        game['captures'] = c.captures_list
        games.append(game)
    return games
    
def get_series_cart():
    gids = []
    with open('++Carrito Series Ingame.txt', 'r+') as std:
        txt = std.readlines()
    for t in txt:
        gids.append(get_id(t))
    series = []
    for i in gids:
        s = sess.query(Serie).get(i)
        genders = []
        for t in s.genders:
            genders.append(t.name)
        actors = []
        for a in s.actors:
            actors.append(a.name)
        directors = []
        for d in s.directors:
            directors.append(d.name)
        serie = {}
        serie['id'] = s.id
        serie['title'] = s.title
        serie['year'] = s.year 
        serie['sinopsis'] = s.sinopsis
        serie['country'] = s.country
        serie['genders'] = genders
        serie['actors'] = actors
        serie['directors'] = directors
        serie['score'] = s.score
        serie['cover_path'] = s.cover_path
        series.append(serie)
    return series

def get_movies_cart():
    gids = []
    with open('++Carrito Movies Ingame.txt', 'r+') as std:
        txt = std.readlines()
    for t in txt:
        gids.append(get_id(t))
    movies = []
    for i in gids:
        s = sess.query(Movie).get(i)
        genders = []
        for t in s.genders:
            genders.append(t.name)
        actors = []
        for a in s.actors:
            actors.append(a.name)
        directors = []
        for d in s.directors:
            directors.append(d.name)
        movie = {}
        movie['id'] = s.id
        movie['title'] = s.title
        movie['year'] = s.year 
        movie['sinopsis'] = s.sinopsis
        movie['country'] = s.country
        movie['genders'] = genders
        movie['actors'] = actors
        movie['directors'] = directors
        movie['score'] = s.score
        movie['cover_path'] = s.cover_path
        movies.append(movie)
    return movies

def edit_games(gs):
    lines = []
    for g in gs:
        lines.append('['+str(g[0])+'] '+g[1]+ '\n')
    with open('++Carrito Juegos Ingame.txt', 'w+') as std:
        txt = std.writelines(lines)

def edit_series(gs):
    lines = []
    for g in gs:
        lines.append('['+str(g[0])+'] '+g[1] + '\n')
    with open('++Carrito Series Ingame.txt', 'w+') as std:
        txt = std.writelines(lines)

def edit_movies(gs):
    lines = []
    for g in gs:
        lines.append('['+str(g[0])+'] '+g[1]+ '\n')
    with open('++Carrito Movies Ingame.txt', 'w+') as std:
        txt = std.writelines(lines)
        

def get_id(string):
    num = ''
    on = False
    for i in string:
        if i == ']':
            on = False
            break
        if on:
            num+=i
        if i == '[':
            on = True
    return int(num)
        

# Add_Game(25)
# Add_Movie(85)
# Add_Serie(102)
# Add_Game(94)
# Add_Movie(43)
# Add_Serie(200)

# print(get_games_cart())
# print()
# print(get_movies_cart())
# print()
# print(get_series_cart())

# gs = [[23,'aaaaaaaa'], [44, 'bbbbbbbbbb']]
# edit_games(gs)
