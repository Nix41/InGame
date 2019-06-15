
from DBstructure import *
import weasyprint as ws
import os


print('Generating PDF')
html_games=('<div style="width:100%; border:solid grey; border-radius: 20px; height:440px; margin-bottom:35px">'
            '<div style="width:30%; height:430px; float:left;">'
                '<img src="{7}" class="img-fluid" style="height: 96%; width:100%; margin-top:10px; margin-left:10px; object-fit: cover; border-radius: 20px;" alt="Responsive image">'
            '</div>'
            '<div style="width:70%; height:430px; float:left;">'
                '<div style="border:solid grey; width:96%; height:60px; border-radius: 20px; margin-top:10px; margin-left:15px; margin-right: 0 !important;">'
                    '<div style="margin-left: 10px; margin-top: 5px;">'
                        '<h3 style="margin:0 !important;">{1}</h3>'
                    '</div>'
                '</div>'
                '<div style="border:solid grey; width:60%; height:345px; float:left; border-radius: 20px; margin-top:5px; margin-left:15px;">'
                    '<div style="margin-left: 10px; margin-top: 15px;">'
                        '<h4 style="margin:0 !important;">Descripción:</h4>'
                    '</div>'
                    '<div style="margin:10px;">'
                        '<p style="font-size:12px;">{2}</p>'
                    '</div>'
                '</div>'
                '<div style="width:36%; height:370px; float:left;">'
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
count = 1
for g in sess.query(Game).all():
        gens = g.category.name + ','
        for gen in g.genders:
                gens += gen.name + ','
        gens = gens[:-1]
        if count%3 == 1:
            s = s + '<h1 style="color:red;">++INGAME++ 7831-11-30</h1>' + html_games.format(g.id, g.name ,g.description, gens,  g.game_mode, g.launch, g.size, 'web/' + g.cover_path)
        else:
            s = s + html_games.format(g.id, g.name ,g.description, gens,  g.game_mode, g.launch, g.size, 'web/' + g.cover_path)
        count = count + 1
css = ws.CSS(string='@page {size: A3; margin-top:10px; margin-bottom:90.4px;}')
ws.HTML(string=s, base_url='./').write_pdf('PDF/Games.pdf', stylesheets=[css])

s = ''
html_series = ('<div style="width:100%; border:solid grey; border-radius: 20px; height:440px; margin-bottom:40px">'
            '<div style="width:30%; height:430px; float:left;">'
                '<img src="{6}" class="img-fluid" style="height: 96%; width:100%; margin-top:10px; margin-left:10px; object-fit: cover; border-radius: 20px;" alt="Responsive image">'
            '</div>'
            '<div style="width:70%; height:430px; float:left;">'
                '<div style="border:solid grey; width:96%; height:30px; border-radius: 20px; margin-top:10px; margin-left:15px; margin-right: 0 !important;">'
                    '<div style="margin-left: 10px; margin-top: 5px;">'
                        '<h3 style="margin:0 !important;">{1}</h3>'
                    '</div>'
                '</div>'
                '<div style="border:solid grey; width:60%; height:345px; float:left; border-radius: 20px; margin-top:5px; margin-left:15px;">'
                    '<div style="margin-left: 10px; margin-top: 15px;">'
                        '<h4 style="margin:0 !important;">Sinopsis:</h4>'
                    '</div>'
                    '<div style="margin:10px;">'
                        '<p style="font-size:12px;">{2}</p>'
                    '</div>'
                '</div>'
                '<div style="width:36%; height:370px; float:left;">'
                    '<div style="border:solid grey; width:97%; border-radius: 20px; margin-top:6px; margin-left:5px; margin-right: 0 !important;">'
                        '<div style="margin-left: 10px; margin-top: 15px;">'
                            '<h4 style="margin:0 !important;">Géneros:</h4>'
                        '</div>'
                        '<div style="margin:10px;">'
                            '<p>{3}'
                            '</p>'
                        '</div>'
                    '</div>'

                    '<div style="border-radius: 20px; margin-top:10px; margin-left:5px; margin-right: 0 !important;">'
                        '<div style="float:left; border:solid grey; width:45%; border-radius: 20px; margin-top:10px; margin-right: 0 !important;">'
                            '<div style="margin-left: 10px; margin-top: 15px;">'
                                '<h4 style="margin:0 !important;">Año:</h4>'
                            '</div>'
                            '<div style="margin:10px;">'
                                '<p>{4}'
                                '</p>'
                            '</div>'
                        '</div>'
                        '<div style="float:left; margin-left: 8px; border:solid grey; width:45%; border-radius: 20px; margin-top:10px; margin-right: 0 !important;">'
                            '<div style="margin-left: 10px; margin-top: 15px;">'
                                '<h4 style="margin:0 !important;">País</h4>'
                            '</div>'
                            '<div style="margin:10px;">'
                                '<p>{5}'
                                '</p>'
                            '</div>'
                        '</div>'
                    '</div>'
                '</div>'
            '</div>'
        '</div>')

count = 1
for g in sess.query(Serie).all():
        gens = ''
        for gen in g.genders:
                gens += gen.name + ', '
        gens = gens[:-2]
        if count%3 == 1:
            s = s + '<h1 style="color:red; margin-top:15px;"">++INGAME++ 7831-11-30</h1>' + html_series.format(g.id, g.title ,g.sinopsis, gens, g.year, g.country, 'web/' + g.cover_path)
        else:
            s = s + html_series.format(g.id, g.title ,g.sinopsis, gens, g.year, g.country, 'web/' + g.cover_path)
        count += 1
css = ws.CSS(string='@page {size: A3; margin-top:0px; margin-bottom:90.4px;}')
ws.HTML(string=s, base_url='./').write_pdf('PDF/Series.pdf', stylesheets=[css])

s = ''

html_movies = ('<div style="width:100%; border:solid grey; border-radius: 20px; height:440px; margin-bottom:40px">'
            '<div style="width:30%; height:430px; float:left;">'
                '<img src="{6}" class="img-fluid" style="height: 96%; width:100%; margin-top:10px; margin-left:10px; object-fit: cover; border-radius: 20px;" alt="Responsive image">'
            '</div>'
            '<div style="width:70%; height:430px; float:left;">'
                '<div style="border:solid grey; width:96%; height:30px; border-radius: 20px; margin-top:10px; margin-left:15px; margin-right: 0 !important;">'
                    '<div style="margin-left: 10px; margin-top: 5px;">'
                        '<h3 style="margin:0 !important;">{1}</h3>'
                    '</div>'
                '</div>'
                '<div style="border:solid grey; width:60%; height:345px; float:left; border-radius: 20px; margin-top:5px; margin-left:15px;">'
                    '<div style="margin-left: 10px; margin-top: 15px;">'
                        '<h4 style="margin:0 !important;">Sinopsis:</h4>'
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

                    '<div style="border-radius: 20px; margin-top:10px; margin-left:5px; margin-right: 0 !important;">'
                        '<div style="float:left; border:solid grey; width:45%; border-radius: 20px; margin-top:10px; margin-right: 0 !important;">'
                            '<div style="margin-left: 10px; margin-top: 15px;">'
                                '<h4 style="margin:0 !important;">Año:</h4>'
                            '</div>'
                            '<div style="margin:10px;">'
                                '<p>{4}'
                                '</p>'
                            '</div>'
                        '</div>'
                        '<div style="float:left; margin-left: 8px; border:solid grey; width:45%; border-radius: 20px; margin-top:10px; margin-right: 0 !important;">'
                            '<div style="margin-left: 10px; margin-top: 15px;">'
                                '<h4 style="margin:0 !important;">País</h4>'
                            '</div>'
                            '<div style="margin:10px;">'
                                '<p>{5}'
                                '</p>'
                            '</div>'
                        '</div>'
                    '</div>'
                '</div>'
            '</div>'
        '</div>')

count = 1
for g in sess.query(Movie).all():
        gens = ''
        for gen in g.genders:
                gens += gen.name + ', '
        gens = gens[:-2]
        if count%3 == 1:
            s = s + '<h1 style="color:red; margin-top:15px;">++INGAME++ 7831-11-30</h1>' + html_movies.format(g.id, g.title ,g.sinopsis, gens, g.year, g.country, 'web/' + g.cover_path)
        else:
            s = s + html_movies.format(g.id, g.title ,g.sinopsis, gens, g.year, g.country, 'web/' + g.cover_path)
        count += 1
css = ws.CSS(string='@page {size: A3; margin-top:0px; margin-bottom:90.4px;}')
ws.HTML(string=s, base_url='./').write_pdf('PDF/Movies.pdf', stylesheets=[css])
print('Done With PDF')
