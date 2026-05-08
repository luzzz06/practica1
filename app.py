from flask import Flask, render_template, request, redirect, url_for, flash, session
from gestor_tareas import Gestortareas

app = Flask(__name__)
app.secret_key = 'mi_llave_secreta_123'
gestor = Gestortareas()

@app.route('/')
def index():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/tareas')
def tareas():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    mis_tareas = gestor.obtener_tareas_usuario(session['usuario_id'])
    return render_template('tareas.html', tareas=mis_tareas)

@app.route('/agregar', methods=['POST'])
def agregar_tarea():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    titulo = request.form.get('tarea')
    if titulo:
        gestor.crear_tarea(session['usuario_id'], titulo, "pendiente")
    return redirect(url_for('tareas'))

@app.route('/actualizar_estado', methods=['POST'])
def actualizar_estado():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    
    tarea_id = request.form.get('id')
    nuevo_estado = request.form.get('nuevo_estado')
    if tarea_id and nuevo_estado in ["pendiente", "en_progreso", "completada", "cancelada"]:
        gestor.actualizar_estado_tarea(tarea_id, nuevo_estado)
        
    return redirect(url_for('tareas'))
@app.route('/eliminar', methods=['POST'])
def eliminar_tarea():
    tarea_id = request.form.get('id')
    if tarea_id:
        gestor.eliminar_tarea(tarea_id)
    return redirect(url_for('tareas'))

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form.get('usuario')
        email = request.form.get('email')
        password = request.form.get('password')
        if gestor.crear_usuario(nombre, email, password):
            flash("Registro exitoso", "success")
            return redirect(url_for('login'))
        flash("El correo ya existe", "danger")
    return render_template('registro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        u = gestor.obtener_usuario_por_email(email)
        if u and u['secreto'] == password:
            session['usuario_id'] = str(u['_id'])
            session['usuario_nombre'] = u['user']
            return redirect(url_for('index'))
        flash("Credenciales incorrectas", "danger")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/metas')
def metas(): return render_template('metas.html')

@app.route('/calendario')
def calendario(): return render_template('calendario.html')

if __name__ == '__main__':
    app.run(debug=True)