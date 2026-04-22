from flask import Flask, render_template, request, redirect, url_for
# Asegúrate de que el archivo gestordetareas.py exista
from gestordetareas import Gestor  

app = Flask(__name__)

tareas_db = []

@app.route('/')
def index():
    return render_template('index.html', tareas=tareas_db)

@app.route('/agregar', methods=['POST'])
def agregar():
    nombre = request.form.get('tarea')
    imagen = request.form.get('url_imagen') 
    if nombre:
        tareas_db.append({'nombre': nombre, 'imagen': imagen})
    return redirect(url_for('index'))

@app.route('/eliminar-tarea', methods=['POST'])
def eliminar():
    tarea_id = request.form.get('id')
    if tarea_id is not None:
        try:
            indice = int(tarea_id)
            if 0 <= indice < len(tareas_db):
                tareas_db.pop(indice)
        except (ValueError, IndexError):
            pass
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST']) 
def register():
    if request.method == 'POST':
        usuario = request.form.get('username')
        # Aquí iría la lógica para guardar en base de datos
        print(f"Registro exitoso: {usuario}")
        return redirect(url_for('login')) # Después de registrarse, mandarlo a loguearse
    return render_template('registro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form.get('email')
        password = request.form.get('password')
        
        # Ejemplo de cómo usarías tu gestor (ajusta según tu clase)
        # gestor = Gestor() 
        # if gestor.obtener_usuario2(correo, password):
        
        if correo == "hola@gmail.com" and password == "1234": # Prueba simple
            print(f"Login exitoso: {correo}")
            return redirect(url_for('index'))
        else:
            # Si los datos están mal, puedes mandarlo a una página de error o recargar login
            return render_template("login.html", error="Credenciales incorrectas")
            
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)