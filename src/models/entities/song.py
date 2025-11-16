"""
Entidad `Song` que representa una canción extraída de la tabla `songs`.

Contiene campos usados por las vistas y por la lógica de tablaturas.
"""


class Song:
    def __init__(self, id, titulo, artista, fecha_publicacion, tiempo, notas, ligaduras, compases, corcheas, tablatura_data=None):
        self.id = id
        self.titulo = titulo
        self.artista = artista
        self.fecha_publicacion = fecha_publicacion
        self.tiempo = tiempo
        self.notas = notas
        self.ligaduras = ligaduras
        self.compases = compases
        self.corcheas = corcheas
        self.tablatura_data = tablatura_data

