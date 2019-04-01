
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
