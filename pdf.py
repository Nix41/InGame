
import pdfkit 
import os
import DBstructure
from DBstructure import sess ,Game

games = sess.query(Game).all()

final = ''' '''

html = ''' 
{0}
'''

for g in games:
    print(html.format(g.name))
    final += html.format(g.name)

slash = '/'
pdfkit.from_string(final,'images.pdf') 

