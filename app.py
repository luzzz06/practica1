from flask import Flask, render_template, request, redirect, url_for, flash
from gestor_tareas import GestorTareas

app = Flask(__name__)
app.secret_key = 'mi_llave_secreta_para_flask'
gestor = GestorTareas() 


tareas_db = []


@app.route('/')
def index():
    return render_template('index.html', tareas=tareas_db)

@app.route('/agregar', methods=['POST'])
def agregar():
    nombre = request.form.get('tarea')
    if nombre and nombre.strip():
        tareas_db.append({'nombre': nombre.strip()})
    return redirect(url_for('index'))

@app.route('/eliminar-tarea', methods=['POST'])
def eliminar():
    tarea_id = request.form.get('id')
    if tarea_id:
        try:
            indice = int(tarea_id)
            if 0 <= indice < len(tareas_db):
                tareas_db.pop(indice)
        except ValueError:
            pass
    return redirect(url_for('index'))

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form.get('usuario')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash("❌ Las contraseñas no coinciden", "danger")
            return redirect(url_for('registro'))

        exito = gestor.crear_usuario(nombre, email, password)
        
        if exito:
            flash(f"¡Bienvenida {nombre}! Tu cuenta ha sido creada ✨", "success")
            return redirect(url_for('login'))
        else:
            flash("❌ El correo ya está registrado o hubo un error", "danger")
            return redirect(url_for('registro'))

    return render_template('registro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form.get('email')
        password = request.form.get('password')
        
        usuario_encontrado = gestor.obtener_usuario_por_email(correo)
        
        if usuario_encontrado and usuario_encontrado['secreto'] == password:
            flash(f"✨ ¡Hola de nuevo! Ya puedes gestionar tus tareas", "success")
            return redirect(url_for('index'))
        else:
            flash("❌ Correo o contraseña incorrectos", "danger")
            
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)