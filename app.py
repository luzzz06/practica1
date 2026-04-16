<<<<<<< HEAD
from flask import Flask, render_template, request, redirect, url_for, flash, session
import requests

app = Flask(__name__)
app.secret_key = "clave_secreta_segura"  


@app.route('/')
def base():
    return render_template('base.html')

@app.route('/tareas')
def tareas():
    return render_template('tareas.html')

@app.route('/registro')
def registroo():
    return render_template('registro.html')


@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        correo = request.form.get("correo").lower()
        if correo in usuarios_registrados:
            flash("Este correo ya está registrado", "danger")
            return redirect(url_for('registro'))
        usuarios_registrados[correo] = {key: request.form.get(key) for key in diccionario_datos}
        flash("Registro exitoso, inicia sesión ahora", "exito")
        return redirect(url_for('iniciar_sesion'))
    return render_template('registro.html')



@app.route('/inicia_sesion', methods=['GET', 'POST'])
def iniciar_sesion():
    if request.method == 'POST':
        correo = request.form.get("correo", "").lower()
        contraseña = request.form.get("contraseña")
        usuario = usuarios_registrados.get(correo)

        if usuario and usuario.get("contraseña") == contraseña:
            session["correo"] = correo
            session["logueado"] = True
            session["usuario"] = usuario.get("nombre", correo)
            flash(f"Bienvenido {usuario.get('nombre')}!", "success")
            return redirect(url_for('inicio'))
        else:
            flash("Correo o contraseña incorrectos", "danger")
            return redirect(url_for('iniciar_sesion'))

    return render_template("login.html")

@app.route('/perfil')
def perfil():
    if not session.get("logueado"):
        flash("Debes iniciar sesión para ver tu perfil.", "warning")
        return redirect(url_for('iniciar_sesion'))

    correo = session.get("correo")
    usuario = usuarios_registrados.get(correo)
    return render_template("perfil.html", usuario=usuario)

@app.route('/logout')
def logout():
    session.clear()
    flash('Has cerrado sesión correctamente', 'info')
    return redirect(url_for('iniciar_sesion'))




if __name__ == '__main__':
    app.run(debug=True)

=======
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

tareas = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        tarea = request.form['tarea']
        tareas.append(tarea)
        return redirect('/')
    return render_template('index.html', tareas=tareas)

if __name__ == '__main__':
    app.run(debug=True)
>>>>>>> 3f410a640a6dd5a141901b03748c4274ea4d47c7
