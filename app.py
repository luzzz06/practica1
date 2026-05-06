from flask import Flask, render_template, request, redirect, url_for, flash, session
from gestor_tareas import GestorTareas

app = Flask(__name__)
app.secret_key = 'mi_llave_secreta_para_flask'
gestor = GestorTareas() 



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tareas')
def tareas():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    
    # Aquí es donde deberías definir tareas_db para que no te de error
    return render_template('tareas.html')


#@app.route('/agregar', methods=['POST'])
#def agregar():
   # nombre = request.form.get('tarea')
  #  if nombre and nombre.strip():
 #       tareas_db.append({'nombre': nombre.strip()})
   # return redirect(url_for('index'))

#@app.route('/eliminar-tarea', methods=['POST'])
#def eliminar():
 #   tarea_id = request.form.get('id')
  #  if tarea_id:
   #     try:
     #       indice = int(tarea_id)
    #        if 0 <= indice < len(tareas_db):
      #          tareas_db.pop(indice)
       # except ValueError:
        #    pass
    #return redirect(url_for('index'))


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