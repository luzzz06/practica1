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

if __name__ == '__main__':
    app.run(debug=True)