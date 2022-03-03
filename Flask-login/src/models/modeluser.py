from .entities import User

class ModelUser():

    @classmethod
    def login(self, db, user):
        try:
            cursor = db.connecrtion.cursor()
            sql = """select id, username, password, fullname FROM usuarios
                    where username = '{}'""".format(user.username)
            cursor.execute(sql)
            row = cursor.fetchone()

            if row != None:
                user = User(row[0], row[1], User.check_password(row[2], user.password), row[3] )
                return user
            else:
                 return None

        except Exception as ex:
            raise Exception(ex)
        finally:
            cursor.close()