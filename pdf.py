
from DBstructure import *
from weasyprint import HTML, CSS
import os

html = ('<div class="d-flex mb-3" style="border: solid rgb(77,77,77); border-radius: 20px;">'
        '<div class=" mr-auto p-2">'
        '<div style="width:240px;height:337px;">'
        '<img src="web/img/Work/Games/{2}image.jpeg" style="width:100%;height:100%;"> '
        '</div>'
        '</div>'
        '<div class="mr-auto p-2" style="margin-left:200px;">'
        '<h2> {0} </h2>'
        '<p> {3} </p>'
        '</div>'
        '</div>')

s = ''
dir = os.path.abspath('./')
print(dir)
for g in sess.query(Game).all():
    s = s + html.format(g.name, dir , g.id, g.description)
css = CSS(filename='./web/css/w3.css')
HTML(string=s, base_url='./').write_pdf('weasyprint-website.pdf', stylesheets=[css])

