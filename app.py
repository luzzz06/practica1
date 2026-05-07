from flask import Flask, render_template, request, redirect, url_for, flash, session
from gestor_tareas import GestorTareas


app = Flask(__name__)
app.secret_key = 'mi_llave_secreta_para_flask'
gestor = GestorTareas() 


tareas_db = []


@app.route('/')
def index():

    return render_template('index.html')

@app.route('/tareas')
def tareas():
    # 1. Traemos las tareas de MongoDB
    lista_tareas = db.obtener_todas()
    # 2. Renderizamos tareas.html (donde pusiste el datalist)
    return render_template('tareas.html', tareas=lista_tareas)


@app.route('/agregar', methods=['POST'])
def agregar():
    titulo = request.form.get('tarea')
    if titulo:
        db.crear_tarea(titulo)
    return redirect(url_for('tareas')) # Te regresa a la lista de tareas

@app.route('/eliminar', methods=['POST'])
def eliminar():
    id_tarea = request.form.get('id')
    if id_tarea:
        db.eliminar_tarea(id_tarea)
    return redirect(url_for('tareas'))




@app.route('/metas')
def metas():
    # Verificamos que el usuario esté logueado (por seguridad)
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    
    # Aquí podrías buscar metas en MongoDB si decides guardarlas ahí después
    return render_template('metas.html')

@app.route('/calendario')
def calendario():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    
    return render_template('calendario.html')



@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form.get('usuario')
        email = request.form.get('email')
        password = request.form.get('password')

        # Registro directo
        if gestor.crear_usuario(nombre, email, password):
            flash("¡Registro exitoso!", "success")
            return redirect(url_for('login'))
        else:
            flash("Error: El correo ya existe", "danger")
            return redirect(url_for('registro'))

    return render_template('registro.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form.get('email')
        password = request.form.get('password')
        
        # Buscamos al usuario en la base de datos
        usuario = gestor.obtener_usuario_por_email(correo)
    
        # Verificamos que el usuario exista y la contraseña ('secreto') coincida
        if usuario and usuario['secreto'] == password:
            session['usuario_id'] = str(usuario['_id'])
            session['usuario_nombre'] = usuario['user'] 
            return redirect(url_for('index'))
        
        flash("Correo o contraseña incorrectos", "danger")
    return render_template('login.html')

@app.route('/logout')
def logout():
    
    session.clear() 
    flash("Has cerrado sesión correctamente", "info")
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)