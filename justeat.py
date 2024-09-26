from flask import Flask,render_template, url_for,request,redirect
from flask_mysqldb import MySQL
from flask_login import LoginManager,login_user,logout_user
from config import config 
from werkzeug.security import generate_password_hash
import datetime


justeat = Flask(__name__)
db = MySQL(justeat)
adminSession = LoginManager(justeat)      

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
    return redirect(url_for('home'))
  else:  
    return render_template('signup.html',methods = {'GET','POST'})

if __name__ == '__main__':
  justeat.config.from_object(config['development'])
  justeat.run(port=3300) 