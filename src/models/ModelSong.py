from .entities.song import Song
import json
import re

class ModelSong():
    @classmethod
    def get_by_id(cls, db, id):
        # Obtiene una canción por su ID (mapea columnas de la tabla `songs`)
        try:
            cursor = db.connection.cursor()
            sql = """SELECT id, title, artist, release_date, bpm, measures, json_file
                     FROM songs WHERE id = %s"""
            cursor.execute(sql, (id,))
            row = cursor.fetchone()
            if row != None:
                return Song(
                    id=row[0],
                    titulo=row[1],
                    artista=row[2],
                    fecha_publicacion=row[3],
                    tiempo=row[4],
                    notas=None,
                    ligaduras=None,
                    compases=row[5],
                    corcheas=None,
                    tablatura_data=row[6] if row[6] else None
                )
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_by_slug(cls, db, cancion_slug):
        # Busca por título (no hay columna slug en la tabla `songs`)
        try:
            cursor = db.connection.cursor()
            sql = """SELECT id, title, artist, release_date, bpm, measures, json_file
                     FROM songs WHERE LOWER(title) = LOWER(%s)"""
            cursor.execute(sql, (cancion_slug,))
            row = cursor.fetchone()
            if row != None:
                return Song(
                    id=row[0],
                    titulo=row[1],
                    artista=row[2],
                    fecha_publicacion=row[3],
                    tiempo=row[4],
                    notas=None,
                    ligaduras=None,
                    compases=row[5],
                    corcheas=None,
                    tablatura_data=row[6] if row[6] else None
                )
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def parse_tablatura_data(cls, tablatura_data):
        # Convierte JSON string a diccionario Python
        if not tablatura_data:
            return None
        try:
            if isinstance(tablatura_data, str):
                return json.loads(tablatura_data)
            return tablatura_data
        except json.JSONDecodeError:
            return None

    @classmethod
    def get_all_songs(cls, db, limit=100):
        # Obtiene todas las canciones ordenadas alfabéticamente
        try:
            cursor = db.connection.cursor()
            sql = """SELECT id, title, artist 
                     FROM songs 
                     ORDER BY title ASC
                     LIMIT %s"""
            cursor.execute(sql, (limit,))
            rows = cursor.fetchall()
            results = []
            for row in rows:
                results.append({
                    'id': row[0],
                    'titulo': row[1],
                    'artista': row[2],
                    'slug': row[1]
                })
            return results
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def search_songs(cls, db, query, limit=10):
        # Busca canciones por título o artista
        try:
            cursor = db.connection.cursor()
            search_term = f"%{query}%"
            sql = """SELECT id, title, artist 
                     FROM songs 
                     WHERE title LIKE %s OR artist LIKE %s 
                     ORDER BY 
                         CASE 
                             WHEN title LIKE %s THEN 1 
                             WHEN artist LIKE %s THEN 2 
                             ELSE 3 
                         END,
                         title ASC
                     LIMIT %s"""
            cursor.execute(sql, (search_term, search_term, search_term, search_term, limit))
            rows = cursor.fetchall()
            results = []
            for row in rows:
                results.append({
                    'id': row[0],
                    'titulo': row[1],
                    'artista': row[2],
                    'slug': row[1]
                })
            return results
        except Exception as ex:
            raise Exception(ex)

