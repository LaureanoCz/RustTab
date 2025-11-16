"""
ModelFavorite - operaciones para gestionar favoritos de usuarios.

Provee métodos para comprobar, añadir y eliminar favoritos, y para
recuperar la lista de ids de canciones favoritas de un usuario.
"""

class ModelFavorite():
    @classmethod
    def is_favorite(cls, db, user_id, song_id):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT 1 FROM favorites WHERE user_id = %s AND song_id = %s LIMIT 1"
            cursor.execute(sql, (user_id, song_id))
            row = cursor.fetchone()
            return row is not None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def add_favorite(cls, db, user_id, song_id):
        try:
            cursor = db.connection.cursor()
            sql = "INSERT INTO favorites (user_id, song_id) VALUES (%s, %s)"
            cursor.execute(sql, (user_id, song_id))
            db.connection.commit()
            return True
        except Exception as ex:
            db.connection.rollback()
            raise Exception(ex)

    @classmethod
    def remove_favorite(cls, db, user_id, song_id):
        try:
            cursor = db.connection.cursor()
            sql = "DELETE FROM favorites WHERE user_id = %s AND song_id = %s"
            cursor.execute(sql, (user_id, song_id))
            db.connection.commit()
            return True
        except Exception as ex:
            db.connection.rollback()
            raise Exception(ex)

    @classmethod
    def get_favorites_by_user(cls, db, user_id):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT song_id FROM favorites WHERE user_id = %s"
            cursor.execute(sql, (user_id,))
            rows = cursor.fetchall()
            return [r[0] for r in rows]
        except Exception as ex:
            raise Exception(ex)
