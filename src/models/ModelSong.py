from .entities.song import Song
import json

class ModelSong():
    @classmethod
    def get_by_id(cls, db, id):
        """Get a song by its ID"""
        try:
            cursor = db.connection.cursor()
            sql = """SELECT id, titulo, artista, fecha_publicacion, tiempo, notas, 
                     ligaduras, compases, corcheas, tablatura_data, slug
                     FROM canciones WHERE id = %s"""
            cursor.execute(sql, (id,))
            row = cursor.fetchone()
            if row != None:
                return Song(
                    id=row[0],
                    titulo=row[1],
                    artista=row[2],
                    fecha_publicacion=row[3],
                    tiempo=row[4],
                    notas=row[5],
                    ligaduras=row[6],
                    compases=row[7],
                    corcheas=row[8],
                    tablatura_data=row[9] if row[9] else None
                )
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def get_by_slug(cls, db, cancion_slug):
        """Get a song by its slug/name (for URL-friendly names)"""
        try:
            cursor = db.connection.cursor()
            sql = """SELECT id, titulo, artista, fecha_publicacion, tiempo, notas, 
                     ligaduras, compases, corcheas, tablatura_data, slug
                     FROM canciones WHERE slug = %s OR titulo = %s"""
            cursor.execute(sql, (cancion_slug, cancion_slug))
            row = cursor.fetchone()
            if row != None:
                return Song(
                    id=row[0],
                    titulo=row[1],
                    artista=row[2],
                    fecha_publicacion=row[3],
                    tiempo=row[4],
                    notas=row[5],
                    ligaduras=row[6],
                    compases=row[7],
                    corcheas=row[8],
                    tablatura_data=row[9] if row[9] else None
                )
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def parse_tablatura_data(cls, tablatura_data):
        """Parse tablatura data from JSON string to Python dict"""
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
        """Get all songs ordered alphabetically"""
        try:
            cursor = db.connection.cursor()
            sql = """SELECT id, titulo, artista, slug 
                     FROM canciones 
                     ORDER BY titulo ASC
                     LIMIT %s"""
            cursor.execute(sql, (limit,))
            rows = cursor.fetchall()
            results = []
            for row in rows:
                results.append({
                    'id': row[0],
                    'titulo': row[1],
                    'artista': row[2],
                    'slug': row[3] if len(row) > 3 and row[3] else row[1].lower().replace(' ', '-').replace('_', '-')
                })
            return results
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def search_songs(cls, db, query, limit=10):
        """Search songs by title or artist"""
        try:
            cursor = db.connection.cursor()
            search_term = f"%{query}%"
            sql = """SELECT id, titulo, artista, slug 
                     FROM canciones 
                     WHERE titulo LIKE %s OR artista LIKE %s 
                     ORDER BY 
                         CASE 
                             WHEN titulo LIKE %s THEN 1 
                             WHEN artista LIKE %s THEN 2 
                             ELSE 3 
                         END,
                         titulo ASC
                     LIMIT %s"""
            # Use the same search_term for all LIKE conditions
            cursor.execute(sql, (search_term, search_term, search_term, search_term, limit))
            rows = cursor.fetchall()
            results = []
            for row in rows:
                results.append({
                    'id': row[0],
                    'titulo': row[1],
                    'artista': row[2],
                    'slug': row[3] if len(row) > 3 and row[3] else row[1].lower().replace(' ', '-').replace('_', '-')
                })
            return results
        except Exception as ex:
            raise Exception(ex)

