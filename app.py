from flask import Flask, render_template, request, redirect, url_for, flash
from gestor_tareas import GestorTareas

app = Flask(__name__)
gestor = GestorTareas()
app.secret_key = 'clave_secreta'  # 🔑 necesario para flash

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
        # 1. Sacamos los datos del formulario
        nombre = request.form.get('usuario')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # 2. Validación rápida: ¿las contraseñas son iguales?
        if password != confirm_password:
            flash("❌ Las contraseñas no coinciden", "danger")
            return redirect(url_for('registro'))

        # 3. Intentamos guardar en la base de datos
        try:
            # Llamamos a tu gestor de MongoDB Atlas
            nuevo_id = gestor.crear_usuario(nombre, email, password)
            
            if nuevo_id:
                flash(f"¡Bienvenida {nombre}! Tu cuenta ha sido creada ✨", "success")
                # ¡ESTA ES LA MAGIA! Te manda al login después de guardar
                return redirect(url_for('login'))
            else:
                flash("❌ No se pudo crear el usuario", "danger")
                return redirect(url_for('registro'))
                
        except Exception as e:
            # Si algo sale mal con MongoDB, aquí nos avisará
            flash(f"Error de conexión: {e}", "danger")
            return redirect(url_for('registro'))

    # Si entran normal (GET), cargamos el template rosa
    return render_template('registro.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form.get('email')
        password = request.form.get('password')
        
        # Aquí puedes buscar en MongoDB Atlas con:
        # usuario_encontrado = gestor.usuarios.find_one({"email": correo})
        
        if correo == "hola@gmail.com" and password == "1234": # Prueba rápida
            flash("✨ ¡Hola de nuevo! Ya podrás cada día tratar de ser tu mejor versión")
            return redirect(url_for('index'))
        else:
            flash("❌ Correo o contraseña incorrectos", "danger")
            
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)