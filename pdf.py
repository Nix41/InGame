
from DBstructure import *
from weasyprint import HTML, CSS
import os

html2=('<div style="width:100%; height:190px; border:solid grey; border-radius: 20px;">'
            '<div style="width:120px;; height:500px;">'
                '<img src="6image.jpeg" class="img-fluid" style="height: 26vw; width:95%; margin-top:10px; margin-left:10px; object-fit: cover; border-radius: 20px;" alt="Responsive image">'
            '</div>'
            '<div style="width:76%; border:solid grey; height:12px; margin-left:140px; margin-top:-490px; border-radius: 20px;">'
                '<div class="container" style="margin-left:20px;">'
                    '<h6 style="margin: 0 !important;">Metro Exodus</h6>'
                '</div>'
            '</div>'
            '<div style="width:50%; margin-left:140px;">'
                '<div style="border:solid grey; border-radius: 20px; margin-top:5px; height: 145px;;">'
                    '<div style="margin-left:20px;">'
                        '<p style="font-size: 10px;">Descripción:</p>'
                    '</div>'
                    '<div class="container" style="max-width:400px; margin:10px; margin-top:-5px; ">'
                        '<p style="font-size: 5.4px;">Vikingos, anglosajones, germanos y eslavos se enfrentan en Ancestors: Legacy, un videojuego de estrategia en tiempo real desarrollado por los autores del polémico Hatred. Comanda a tus tropas, saca partido de sus habilidades especiales, y derrota a tus enemigos en las espectaculares y emocionantes batallas de este juego ambientado en la Edad Media. '
                                'Destructive Creations apuesta por un estilo de juego similar al de Company of Heroes, poniéndote a los mandos de pequeños escuadrones de soldados con sus propias habilidades. En Ancestors: Legacy también es importante sacar provecho del escenario usando la hierba para ocultarte y así atacar por sorpresa a los rivales, o bien creando trampas con las que liquidar al ejército rival con suma efectividad. Por el camino debes gestionar los recursos en las aldeas que conquistes, construyendo edificios para entrenar nuevas tropas.'
                                'Ancestors: Legacy incluye un completo modo campaña con historias protagonizadas por las cuatro facciones que se enfrentan en este videojuego. También podéis combatir contra la IA del juego en escaramuzas, o bien enfrentaros a otros jugadores a través del multijugador online para hasta seis personas.</p>'
                    '</div>'
                '</div>'
            '</div>'
            '<div style="width:185px; margin-left:63%; margin-top: -146px;">'
                '<div style="border:solid grey; border-radius: 20px; margin-left:20px; margin-right:5px;">'
                    '<div style="margin-left:20px;">'
                        '<p style="font-size: 10px;">Géneros:</p>'
                    '</div>'
                    '<div class="container" style="max-width:185px; margin-left:15px; margin-right:5px; margin-top: -8px;">'
                        '<p style="font-size: 5.4px;">aaaaaaaaaaaaaa</p>'
                    '</div>'
                '</div>'
            '</div>'
            '<div style="width:185px; margin-left:431px; margin-top:5px;">'
                '<div style="border:solid grey; border-radius: 20px; margin-left:20px; margin-right:5px;">'
                    '<div style="margin-left:20px;">'
                        '<p style="font-size: 10px;">Modo de Juego:</p>'
                    '</div>'
                    '<div class="container" style="max-width:185px; margin-left:15px; margin-right:5px; margin-top: -8px;">'
                        '<p style="font-size: 5.4px;">aaaaaaaaaaaaaaaaaaaa</p>'
                    '</div>'
                '</div>'
            '</div>'
            '<div style="width:90px;; height:70px; margin-left:431px; margin-top: 5px;">'
                '<div style="border:solid grey; border-radius: 20px; margin-left:20px; margin-right:5px;">'
                    '<div style="margin-left:5px; margin-top: 10px;">'
                        '<p style="font-size: 10px;">Lanzamiento:</p>'
                    '</div>'
                    '<div class="container" style="max-width:200px; margin-left:5px; margin-right:5px; margin-top: -8px; text-align:center;">'
                        '<p style="font-size: 5.4px;">2015</p>'
                    '</div>'
                '</div>'
            '</div>'
            '<div style="width:118px;; height:70px; margin-left:498px; margin-top: -70px;">'
                '<div style="border:solid grey; border-radius: 20px; margin-left:20px; margin-right:5px;">'
                    '<div style="margin-left:5px; margin-top: 10px;">'
                        '<p style="font-size: 10px;">Capacidad en disco:</p>'
                    '</div>'
                    '<div class="container" style="max-width:200px; margin-left:5px; margin-right:5px; margin-top: -8px; text-align:center;">'
                        '<p style="font-size: 5.4px;">2015</p>'
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
css = CSS(string='@page {size: A3;}')
HTML(string=s, base_url='./').write_pdf('Games.pdf', stylesheets=[css])

