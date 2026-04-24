from flask import Flask, render_template, request, redirect, url_for, flash


app = Flask(__name__)
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

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        usuario = request.form.get('username')

        if usuario:
            
            flash(f"Registro exitoso, bienvenido {usuario} 🎉", "success")
            return redirect(url_for('login'))

    return render_template('registro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None

    if request.method == 'POST':
        correo = request.form.get('email')
        password = request.form.get('password')

        if correo == "hola@gmail.com" and password == "1234":
            # --- AQUÍ LANZAS EL MENSAJE ---
            flash("¡Hola, bienvenido! Ya podrás cada día tratar de ser tu mejor versión ✨")
            return redirect(url_for('index'))
        else:
            error = "Datos incorrectos"

    return render_template('login.html', error=error)
if __name__ == '__main__':
    app.run(debug=True)