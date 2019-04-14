
from DBstructure import *
from weasyprint import HTML, CSS
import os

html2=('<div style="width:100%; border:solid grey; border-radius: 20px; height:500px; margin-bottom:11px">'
            '<div style="width:30%; height:500px; float:left;">'
                '<img src="web/img/Work/Games/{0}image.jpeg" class="img-fluid" style="height: 96%; width:100%; margin-top:10px; margin-left:10px; object-fit: cover; border-radius: 20px;" alt="Responsive image">'
            '</div>'
            '<div style="width:70%; height:500px; float:left;">'
                '<div style="border:solid grey; width:96%; height:30px; border-radius: 20px; margin-top:10px; margin-left:15px; margin-right: 0 !important;">'
                    '<div style="margin-left: 10px; margin-top: 5px;">'
                        '<h3 style="margin:0 !important;">{1}</h3>'
                    '</div>'
                '</div>'
                '<div style="border:solid grey; width:60%; height:435px; float:left; border-radius: 20px; margin-top:5px; margin-left:15px;">'
                    '<div style="margin-left: 10px; margin-top: 15px;">'
                        '<h4 style="margin:0 !important;">Descripción:</h4>'
                    '</div>'
                    '<div style="margin:10px;">'
                        '<p style="font-size:12px;">{2}</p>'
                    '</div>'
                '</div>'
                '<div style="width:36%; height:440px; float:left;">'
                    '<div style="border:solid grey; width:97%; border-radius: 20px; margin-top:6px; margin-left:5px; margin-right: 0 !important;">'
                        '<div style="margin-left: 10px; margin-top: 15px;">'
                            '<h4 style="margin:0 !important;">Géneros:</h4>'
                        '</div>'
                        '<div style="margin:10px;">'
                            '<p>{3}'
                            '</p>'
                        '</div>'
                    '</div>'
                    '<div style="border:solid grey; width:97%; border-radius: 20px; margin-top:10px; margin-left:5px; margin-right: 0 !important;">'
                        '<div style="margin-left: 10px; margin-top: 15px;">'
                            '<h4 style="margin:0 !important;">Modalidad:</h4>'
                        '</div>'
                        '<div style="margin:10px;">'
                            '<p>{4}'
                            '</p>'
                        '</div>'
                    '</div>'
                    '<div style="border-radius: 20px; margin-top:10px; margin-left:5px; margin-right: 0 !important;">'
                        '<div style="float:left; border:solid grey; width:45%; border-radius: 20px; margin-top:10px; margin-right: 0 !important;">'
                            '<div style="margin-left: 10px; margin-top: 15px;">'
                                '<h4 style="margin:0 !important;">Fecha:</h4>'
                            '</div>'
                            '<div style="margin:10px;">'
                                '<p>{5}'
                                '</p>'
                            '</div>'
                        '</div>'
                        '<div style="float:left; margin-left: 8px; border:solid grey; width:45%; border-radius: 20px; margin-top:10px; margin-right: 0 !important;">'
                            '<div style="margin-left: 10px; margin-top: 15px;">'
                                '<h4 style="margin:0 !important;">Espacio en disco:</h4>'
                            '</div>'
                            '<div style="margin:10px;">'
                                '<p>{6} GB'
                                '</p>'
                            '</div>'
                        '</div>'
                    '</div>'
                '</div>'
            '</div>'
        '</div>')


s = ''
dir = os.path.abspath('./')
print(dir)
for g in sess.query(Game).all():
        gens = g.category.name + ','
        for gen in g.genders:
                gens += gen.name + ','
        gens = gens[:-1]
        s = s + html2.format(g.id, g.name ,g.description, gens,  g.game_mode, g.launch, g.size)
css = CSS(string='@page {size: A3; margin-top:0px; margin-bottom:39.4px;}')
HTML(string=s, base_url='./').write_pdf('Games.pdf', stylesheets=[css])

