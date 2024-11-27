from flask import Flask,render_template,url_for,request,redirect,flash, session
from flask_mysqldb import MySQL
from flask_login import LoginManager, login_user, logout_user
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash
import random
import string
import datetime
from config import Config
from models.ModelUser import  ModelUser
from models.entities.User import   User


justeatApp = Flask(__name__)
#python enewere dfdf
justeatApp.config.from_object(config['development'])
justeatApp.config.from_object(config['mail'])
db = MySQL(justeatApp)
mail = Mail(justeatApp)
adminSesion = LoginManager(justeatApp)

@adminSesion.user_loader
def cargarUsuario(id):
    return ModelUser.get_by_id(db, id)

@justeatApp.route('/')
def home():
    '''if session['NombreU']:
        if session['PerfilU'] == 'A':
            return render_template('admin.html')
        else:
            return render_template('user.html')'''
    return render_template('home.html')

@justeatApp.route('/signup',methods=['GET','POST'])
def signup():
    if request.method=='POST':
        nombre=request.form['nombre']
        correo=request.form['correo']
        clave=request.form['clave']
        claveCifrada=generate_password_hash(clave)
        fechareg=datetime.datetime.now()
        regUsuario=db.connection.cursor()
        regUsuario.execute("INSERT INTO usuario (nombre, correo, clave, fechareg) VALUES (%s,%s,%s,%s)",(nombre, correo, claveCifrada, fechareg))
        db.connection.commit()
        msg=Message(subject='Bienvenido a justeat, disfruta de tus juegos', recipients=[correo])
        msg.html = render_template('mail.html', nombre = nombre)
        mail.send(msg)
        return render_template('home.html')
    else:
        return render_template('signup.html')
        
    
@justeatApp.route('/signin', methods=['GET','POST'])
def signin():
    if request.method == 'POST':
        usuario = User(0, None, request.form['correo'], request.form['clave'], None,  None)
        usuarioAutenticado =  ModelUser.signin(db,  usuario)
        if usuarioAutenticado is not None:
            login_user(usuarioAutenticado)
            session['NombreU'] = usuarioAutenticado.nombre
            session['Perfil.U']  = usuarioAutenticado.perfil
            if  usuarioAutenticado.clave:
                if usuarioAutenticado.perfil == 'A':
                    return render_template('admin.html')
                else:
                    return render_template('user.html')
            else:
                flash('CONTRASEÑA INCORRECTA')
                return redirect(request.url)
        else:
            flash('CORREO INCORRECTO')
            return redirect(request.url)
    else:
        return render_template('signin.html')

@justeatApp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        correo = request.form['correo']
        # Verificar si el correo existe en la base de datos
        cursor = db.connection.cursor()
        cursor.execute("SELECT id, correo FROM usuario WHERE correo = %s", (correo,))
        usuario = cursor.fetchone()
        cursor.close()

        if usuario:
            # Generar un enlace de restablecimiento único
            token = ''.join(random.choices(string.ascii_letters + string.digits, k=20))

            # Guardar el token en la base de datos para validarlo más tarde
            cursor = db.connection.cursor()
            cursor.execute("UPDATE usuario SET reset_token = %s WHERE correo = %s", (token, correo))
            db.connection.commit()
            cursor.close()

            # Enviar un correo con el enlace de restablecimiento
            reset_url = url_for('reset_password', token=token, _external=True)  # URL con token para restablecer
            msg = Message(subject='Restablecer contraseña', recipients=[correo])
            msg.body = f'Haz clic en el siguiente enlace para restablecer tu contraseña: {reset_url}'
            mail.send(msg)

            flash('Te hemos enviado un correo con instrucciones para restablecer tu contraseña.', 'success')
            return redirect(url_for('signin'))
        else:
            flash('El correo no está registrado.', 'danger')

    return render_template('forgot_password.html')

@justeatApp.route('/reset-password/<token>', methods=['GET', 'POST'], strict_slashes=False)
def reset_password(token):
    # Verificar si el token es válido
    cursor = db.connection.cursor()
    cursor.execute("SELECT id FROM usuario WHERE reset_token = %s", (token,))
    usuario = cursor.fetchone()
    cursor.close()

    if not usuario:
        flash('El enlace de restablecimiento no es válido o ha expirado.', 'danger')
        return redirect(url_for('signin'))
    if request.method == 'POST':
        nueva_clave = request.form['clave']
        hashed_password = generate_password_hash(nueva_clave)
        cursor = db.connection.cursor()
        cursor.execute("UPDATE usuario SET clave = %s, reset_token = NULL WHERE reset_token = %s", (hashed_password, token))
        db.connection.commit()
        cursor.close()
        flash('Tu contraseña ha sido actualizada con éxito.', 'success')
        return redirect(url_for('signin'))
    return render_template('reset_password.html')

@justeatApp.route('/signout', methods=['GET', 'POST'])
def signout():
    session.pop('cart', None)
    logout_user()
    return render_template('home.html')

@justeatApp.route('/sUsuario', methods=['GET','POST'])
def sUsuario():
    selUsuario = db.connection.cursor()
    selUsuario.execute("SELECT * FROM usuario")
    u = selUsuario.fetchall()
    selUsuario.close()
    return render_template('usuarios.html', usuarios = u)

@justeatApp.route('/iUsuario', methods=['GET', 'POST'])
def iUsuario():
    nombre = request.form['nombre']
    correo = request.form['correo']
    clave = request.form['clave']
    claveCifrada = generate_password_hash(clave)
    fechareg = datetime.datetime.now()
    perfil = request.form['perfil']
    creaUsuario= db.connection.cursor()
    creaUsuario.execute("INSERT INTO usuario (nombre, correo, clave, fechareg, perfil) VALUES (%s,%s,%s,%s,%s)", (nombre, correo, claveCifrada, fechareg, perfil))
    db.connection.commit()
    flash('usuario creado')
    return redirect('/sUsuario')

@justeatApp.route('/uUsuario/<int:id>', methods=['GET', 'POST'])
def uUsuario(id):
    nombre = request.form['nombre']
    correo = request.form['correo']
    clave = request.form['clave']
    claveCifrada = generate_password_hash(clave)
    fechareg = datetime.datetime.now()
    perfil = request.form['perfil']
    editarUsuario= db.connection.cursor()
    editarUsuario.execute("UPDATE usuario SET nombre=%s, correo=%s, clave=%s, fechareg=%s, perfil=%s WHERE id=%s", (nombre, correo, claveCifrada, fechareg, perfil, id))
    db.connection.commit()
    flash('Usuario Actualizado')
    return redirect('/sUsuario')

@justeatApp.route("/dUsuario/<int:id>", methods=['GET', 'POST'])
def dUsuario(id):
    eliminarusuario = db.connection.cursor()
    eliminarusuario.execute("DELETE FROM usuario WHERE id = %s", (id,))
    db.connection.commit()
    flash('Usuario Eliminado')
    return redirect('/sUsuario')

@justeatApp.route('/sProducto',  methods=['GET', 'POST'])
def sProducto():
    selProducto=db.connection.cursor()
    selProducto.execute("SELECT * FROM productos")
    p=selProducto.fetchall()
    selProducto.close()
    return render_template('productos.html', productos=p)

@justeatApp.route('/catalogo',  methods=['GET', 'POST'])
def catalogo():
    selcat=db.connection.cursor()
    selcat.execute("SELECT * FROM productos")
    c=selcat.fetchall()
    selcat.close()
    return render_template('user.html', productos=c)

@justeatApp.route('/add-to-cart', methods=['POST'])
def add_to_cart():
    idp=int(request.form['idproducto'])
    selProducto=db.connection.cursor()
    selProducto.execute("SELECT idproducto, nombre, precio, imagen FROM productos WHERE idproducto = %s", (idp,))
    pc=selProducto.fetchone()
    selProducto.close()
    if not pc:
        return redirect('/catalogo')
    cart = session.get('cart', [])
    for item in cart:
        if item['idproducto'] == idp:
            item['cantidad'] += 1
            break
    else:
        cart.append({
            'idproducto': pc[0],
            'nombre': pc[1],
            'precio': pc[2],
            'imagen': pc[3],
            'cantidad': 1
        })
    session['cart']=cart
    return redirect('/catalogo')

@justeatApp.route('/remove-from-cart', methods=['POST'])
def remove_from_cart():
    idp = int(request.form['idproducto'])
    cart = session.get('cart', [])
    session['cart'] = [item for item in cart if item['idproducto'] != idp]
    return redirect('/view_cart')

@justeatApp.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        tarjeta = request.form['tarjeta']
        vencimiento = request.form['vencimiento']
        cvv = request.form['cvv']
        nombre_titular = request.form['nombre_titular']
        return redirect('/direccion')
    return render_template('checkout.html')

@justeatApp.route('/direccion', methods=['GET', 'POST'])
def direccion():
    if request.method == 'POST':
        nombre = request.form['nombre']
        direccion = request.form['direccion']
        ciudad = request.form['ciudad']
        codigopostal = request.form['codigopostal']
        correo = request.form['correo']
        cart=session.get('cart', [])
        total=sum(item['precio'] * item['cantidad'] for item in cart)
        msg=Message(subject='Gracias por tu compra', recipients=[correo])
        msg.html = render_template('mail2.html', nombre=nombre, productos=cart, total=total)
        mail.send(msg)
        return redirect('/gracias')
    return render_template('direccion.html')

@justeatApp.route('/gracias')
def gracias():
    return render_template('gracias.html')

@justeatApp.route('/cart', methods=['GET', 'POST'])
def view_cart():
    cart = session.get('cart', [])
    '''
    print("Contenido del carrito:", cart)
    print(session)
    '''
    cart_valid = [item for item in cart if 'precio' in item and 'cantidad' in item]
    if len(cart) != len(cart_valid):
        print("Elementos inválidos encontrados y excluidos:", [item for item in cart if item not in cart_valid])
    total=sum(item['precio']*item['cantidad'] for item in cart)
    return render_template('cart.html', cart=cart, total=total)

@justeatApp.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    if query:
        selProducto = db.connection.cursor()
        selProducto.execute("SELECT * FROM productos WHERE nombre LIKE %s", ('%' + query + '%',))
        productos = selProducto.fetchall()
        selProducto.close()
    else:
        productos = []
    
    return render_template('user.html', productos=productos)

@justeatApp.route('/iProducto', methods=['GET', 'POST'])
def iProducto():
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    precio = request.form['precio']
    categoria = request.form['categoria']
    existencias = request.form['existencias']
    imagen = request.form['imagen']
    creaProducto= db.connection.cursor()
    creaProducto.execute("INSERT INTO productos (nombre, descripcion, precio, categoria, existencias, imagen) VALUES (%s,%s,%s,%s,%s,%s)", (nombre, descripcion, precio, categoria, existencias, imagen))
    db.connection.commit()
    flash('Producto creado')
    return redirect('/sProducto')

@justeatApp.route('/uProducto/<int:id>', methods=['GET', 'POST'])
def uProducto(id):
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    precio = request.form['precio']
    categoria = request.form['categoria']
    existencias = request.form['existencias']
    imagen = request.form['imagen']
    editarProducto= db.connection.cursor()
    editarProducto.execute("UPDATE productos SET nombre=%s, descripcion=%s, precio=%s, categoria=%s, existencias=%s, imagen=%s WHERE idproducto=%s", (nombre, descripcion, precio, categoria, existencias, imagen, id))
    db.connection.commit()
    flash('Producto Actualizado')
    return redirect('/sProducto')

@justeatApp.route("/dProducto/<int:id>", methods=['GET', 'POST'])
def dProducto(id):
    eliminarProducto = db.connection.cursor()
    eliminarProducto.execute("DELETE FROM productos WHERE idproducto = %s", (id,))
    db.connection.commit()
    flash('Producto Eliminado')
    return redirect('/sProducto')

'''
if __name__ == '__main__':
    justeatApp.config.from_object(config['development'])
    justeatApp.run(port=3300)
'''
if __name__ == "__main__":
    justeatApp.run(host="0.0.0.0", port=5000, debug=True)