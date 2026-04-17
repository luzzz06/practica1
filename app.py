from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

tareas_db = []

@app.route('/')
def index():
    return render_template('index.html', tareas=tareas_db)

@app.route('/agregar', methods=['POST'])
def agregar():
    nueva_tarea = request.form.get('tarea')
    if nueva_tarea:
        tareas_db.append(nueva_tarea)
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST']) 
def register():
    if request.method == 'POST':
        usuario = request.form.get('username')
        print(f"Registro exitoso: {usuario}")
       
        return redirect(url_for('index')) 
    return render_template('registro.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form.get('email')
        password = request.form.get('password')
        print(f"Login: {correo}")
        return redirect(url_for('index')) 
    return render_template('login.html')



if __name__ == '__main__':
    app.run(debug=True)