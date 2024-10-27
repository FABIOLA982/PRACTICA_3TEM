from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Cambia esto por una clave secreta real

# Inicializar la sesión
@app.before_request
def initialize_session():
    if 'inscritos' not in session:
        session['inscritos'] = []

# Ruta principal
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para registrar inscritos
@app.route('/registrar', methods=['POST'])
def registrar():
    fecha = request.form['fecha']
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    turnos = request.form.getlist('turno')
    seminarios = request.form.getlist('seminarios')
    
    nuevo_inscrito = {
        'id': len(session['inscritos']) + 1,
        'fecha': fecha,
        'nombre': nombre,
        'apellido': apellido,
        'turno': ', '.join(turnos),
        'seminarios': ', '.join(seminarios)
    }
    
    session['inscritos'].append(nuevo_inscrito)
    session.modified = True  # Asegura que la sesión se actualice
    return redirect(url_for('inscritos'))

# Ruta para mostrar la lista de inscritos
@app.route('/inscritos')
def inscritos():
    return render_template('inscritos.html', inscritos=session['inscritos'])

# Ruta para eliminar un inscrito
@app.route('/eliminar/<int:id>')
def eliminar(id):
    session['inscritos'] = [inscrito for inscrito in session['inscritos'] if inscrito['id'] != id]
    session.modified = True
    return redirect(url_for('inscritos'))

# Ruta para editar un inscrito (básicamente se redirige al formulario con los datos)
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    if request.method == 'POST':
        for inscrito in session['inscritos']:
            if inscrito['id'] == id:
                inscrito['fecha'] = request.form['fecha']
                inscrito['nombre'] = request.form['nombre']
                inscrito['apellido'] = request.form['apellido']
                inscrito['turno'] = ', '.join(request.form.getlist('turno'))
                inscrito['seminarios'] = ', '.join(request.form.getlist('seminarios'))
                break
        session.modified = True
        return redirect(url_for('inscritos'))

    inscrito = next(inscrito for inscrito in session['inscritos'] if inscrito['id'] == id)
    return render_template('index.html', inscrito=inscrito)

if __name__ == '_main_':
    app.run(debug=True)