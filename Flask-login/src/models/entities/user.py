from werkzeug.security import check_password_hash, generate_password_hash

class User():
    def __init__(self, id, username, password, fullname=""):
        self.id = id
        self.username = username
        self.password = password
        self.fullname = fullname

@classmethod # permite utilizar el método sin instanciar la clase
def check_password(self, hashed_password, password):
    return check_password_hash(hashed_password, password)

# generamos el hash de la pass para almacenarlo en BD
print(generate_password_hash("123456"));