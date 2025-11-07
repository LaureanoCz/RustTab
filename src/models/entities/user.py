from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin): 
    def __init__(self, id, username, password, email): 
        self.id = id 
        self.username = username 
        self.password = password 
        self.email = email

    @staticmethod
    def check_password(hash_password, password): 
        return check_password_hash(hash_password, password)