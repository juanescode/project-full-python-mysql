from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Crear la conexión a la DB
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='python_db'
    )

@app.route('/')
def index():
    conexion = get_db_connection()
    cursor = conexion.cursor(dictionary=True)  # Usar dictionary=True para obtener resultados como diccionarios
    cursor.execute("SELECT * FROM equipos")
    equipos = cursor.fetchall()
    cursor.close()
    conexion.close()
    return render_template('sitio/index.html', equipos=equipos)

@app.route('/sitio/guardar', methods=['POST'])
def guardar():
    descripcion = request.form['descripcion']
    email = request.form['email']
    sql = "INSERT INTO equipos (descripcion, email) VALUES (%s, %s)"
    datos = (descripcion, email)
    conexion = get_db_connection()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()
    cursor.close()
    conexion.close()
    return redirect('/')

@app.route('/sitio/eliminar/<int:id>')
def eliminar(id):
    conexion = get_db_connection()
    cursor = conexion.cursor()
    cursor.execute(f"DELETE FROM equipos WHERE codigo={id}")
    conexion.commit()
    cursor.close()
    conexion.close()
    return redirect('/')

@app.route('/sitio/editar/<int:id>')
def editar(id):
    conexion = get_db_connection()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM equipos WHERE codigo={id}")
    equipo = cursor.fetchone()
    cursor.close()
    conexion.close()
    return render_template('sitio/editar.html', equipo=equipo)

@app.route('/sitio/actualizar/<int:codigo>', methods=['POST'])
def actualizar(codigo):
    if request.method == 'POST':
        email = request.form['email']
        descripcion = request.form['descripcion']
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE equipos
            SET descripcion=%s, email=%s
            WHERE codigo=%s
        """, (descripcion, email, codigo))
        conexion.commit()
        cursor.close()
        conexion.close()
    return redirect('/')

@app.route('/')
def home():
    return render_template('sitio/index.html')

@app.route('/usuarios')
def usuarios():
    conexion = get_db_connection()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute('SELECT * FROM usuarios')
    myresult = cursor.fetchall()
    cursor.close()
    conexion.close()
    return render_template('sitio/usuarios.html', data=myresult)

@app.route('/user', methods=['POST'])
def addUser():
    username = request.form['username']
    password = request.form['password']

    if username and password:
        conexion = get_db_connection()
        cursor = conexion.cursor()
        sql = "INSERT INTO usuarios (username, password) VALUES (%s, %s)"
        data = (username, password)
        cursor.execute(sql, data)
        conexion.commit()
        cursor.close()
        conexion.close()
    return redirect(url_for('usuarios'))

@app.route('/delete/<string:id>')
def delete(id):
    conexion = get_db_connection()
    cursor = conexion.cursor()
    sql = "DELETE FROM usuarios WHERE id=%s"
    data = (id,)
    cursor.execute(sql, data)
    conexion.commit()
    cursor.close()
    conexion.close()
    return redirect(url_for('usuarios'))

@app.route('/edit/<string:id>', methods=['POST'])
def edit(id):
    username = request.form['username']
    password = request.form['password']

    if username and password:
        conexion = get_db_connection()
        cursor = conexion.cursor()
        sql = "UPDATE usuarios SET username = %s, password = %s WHERE id = %s"
        data = (username, password, id)
        cursor.execute(sql, data)
        conexion.commit()
        cursor.close()
        conexion.close()
    return redirect(url_for('usuarios'))

@app.route('/introduccion')
def introduccion():
    return render_template('sitio/introduccion.html')

if __name__ == '__main__':
    app.run(debug=True)




