from .entities.user import User
from werkzeug.security import generate_password_hash

class ModelUser():
    @classmethod
    def login(self, db, user):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT id_user, username, password, email FROM users WHERE username = %s"
            cursor.execute(sql, (user.username,))
            row = cursor.fetchone()

            if row is not None:
                password_correct = User.check_password(row[2], user.password)
                if password_correct:
                    return User(row[0], row[1], row[2], row[3])
            
            return None

        except Exception as ex:
            raise Exception(ex)


    @classmethod
    def get_by_id(cls, db, id):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT id_user, username, email FROM users WHERE id_user = %s"
            cursor.execute(sql, (id,))
            row = cursor.fetchone()
            if row != None:
                return User(row[0], row[1], None, row[2])
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def user_exists(cls, db, username=None, email=None):
        """Check if a user with the given username or email already exists"""
        try:
            cursor = db.connection.cursor()
            if username:
                sql = "SELECT id_user FROM users WHERE username = %s"
                cursor.execute(sql, (username,))
                if cursor.fetchone():
                    return True
            if email:
                sql = "SELECT id_user FROM users WHERE email = %s"
                cursor.execute(sql, (email,))
                if cursor.fetchone():
                    return True
            return False
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def create_user(cls, db, username, email, password):
        """Create a new user in the database"""
        try:
            # Hash the password before storing
            hashed_password = generate_password_hash(password)
            cursor = db.connection.cursor()
            sql = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
            cursor.execute(sql, (username, email, hashed_password))
            db.connection.commit()
            return True
        except Exception as ex:
            db.connection.rollback()
            raise Exception(ex)