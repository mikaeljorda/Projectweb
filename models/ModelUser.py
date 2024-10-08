from models.entities.User import User
from flask_login import login_user

class ModelUser:
    @classmethod
    def signin(self,db,usuario):
        try:
            SelUsiario = db.connection.cursor()
            SelUsiario.execute("SELECT * FROM usuario WHERE correo = %s ",(usuario.correo,))
            U = SelUsiario.fethone()
            if u is not None:
                return User (U[0],u[1],u[2],User(u[3],u[4],u[5])
            
            else:
                return None
        except Exception as ex:
            raise Exception (ex)
        
    @classmethod
    def get_by_id(self,db,id):
        try:
            Selusuario = db.connection.cursor()
            Selusuario.execute("SELECT * FROM usuario WHERE id = %s")
            u = Selusuario.fetchone()
            if u is not None:
                return User(u[0],u[1],u[2],u[3],u[4],u[5])
            else:
                return None
        except Exception as ex:
            raise Exception (ex)
