from flask import Flask,render_template, url_for,request,redirect
from flask_mysqldb import MySQL
from flask_login import LoginManager,login_user,logout_user
from flask_mail import Mail,Messasge
from config import config 
from werkzeug.security import generate_password_hash
import datetime
from models.ModelUser import ModelUser
from models.entities.User import User


@justeat = flask(__name__)
db = MySQL(justeat)
adminSession = LoginManager(justeat)      
#pythonanywhere
@adminSession.user_loader
def signinuser(id):
  return ModelUser.get_by_id(db,id)


@justeat.route('/')
def home():
  return render_template('home.html')

@justeat.route('/signup')
def signup():
  if request.method == 'POST': 
    nombre = request.form['nombre']
    coreo = request.form ['correo']
    clave = generate_password_hash( request.form ['clave'])
    fechareg = datetime.datatime.now()
    regUsiario = db.connection.cursor()
    regUsiario.execute("INSERT INTO usuario(nombre,correo,clave,fechareg) VALUES (%s,%s,%s,%s) ",(nombre,coreo,clave,fechareg))
    db.connection.coomit()
    msg = Messasge{subject ='Gracias por registrate a justeat',recipients=}
    msg.html = render render_template('mail.html',nombre = nombre)
    mail.send(msg)
    return redirect(url_for('home'))
  else:  
    return render_template('signup.html',methods = {'GET','POST'})

@justeat.route('/signin' methods = ['GET','POST'])
def signin():
  if request.method =='POST':
    usuario = User(0, None, request.form['correo'], request.form[clave], None ,None)
    usuarioAuntenticado = ModelUser.signin(db, usuario)
    if usuarioAuntenticado is not None :
      login_user(usuarioAuntenticado)
      if usuarioAuntenticado.clave:
        if usuarioAuntenticado.perfil == 'A':
          return render_template ('admin.html')
        else:
          return render_template('User.html')
      else:
        return 'contraseña incorrecta'
    else:
      return 'usuario inexistente'
  else:
      return render_template('signin,html')
@justeat.route('/sigout',methods=['GET','POST'])
def  signout():
  logout_user  ()
  return render_template('home.html')
@justeat.route("usuario",methods = ['GET','POST'])
def usuario():
  selusuario db.connection.cursor()
  selusuario . execute("SELECT FROM usuario")
  selusuario . fetchall()
  return render_template("usuarios,html",usuario - u)

@justeat.route('/iUsuario',methods = {'GET','POST'})
def iUsuario():
  nombre = request.form['nombre']
  correo = request.form['correo']
  ClaveCifrada = generate_password_hash(request.form['clave'])
  fechareg     = datetime.datetime.now()
  perfil       = request.form['perfil']
  regUsuario   = db.connection.cursor()
  regUsuario.execute("INSERT INTO usuario(nombre.correo,clave,fechareg,perfil)VALUES (%s.%s,%s,%s,%s)"(nombre,correo,ClaveCifrada,fechareg,perfil))
  db.connection.commit() 
  regUsuario.close
#localhost
if __name__ == '__main__': 
  justeat.config.from_object(config['development'])
  justeat.run(port=3300)