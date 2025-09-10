# app.py actualizado con todas las mejoras solicitadas

from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory
import sqlite3
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'secret'
UPLOAD_FOLDER = 'static/uploads'
COMPROBANTES_FOLDER = 'static/comprobantes'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(COMPROBANTES_FOLDER, exist_ok=True)

# --- Funciones auxiliares ---
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def crear_tablas():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS profesores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            carnet TEXT UNIQUE,
            contrasena TEXT,
            turno TEXT,
            especialidad TEXT,
            foto TEXT
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS licencias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            profesor_id INTEGER,
            fecha TEXT,
            motivo TEXT,
            estado TEXT DEFAULT 'En espera',
            fecha_inicio TEXT,
            fecha_fin TEXT,
            archivo TEXT,
            FOREIGN KEY (profesor_id) REFERENCES profesores(id)
        )
    ''')
    admin = conn.execute('SELECT * FROM profesores WHERE carnet = ?', ('admin',)).fetchone()
    if not admin:
        conn.execute('''
            INSERT INTO profesores (nombre, carnet, contrasena, turno, especialidad)
            VALUES (?, ?, ?, ?, ?)
        ''', ('Administrador', 'admin', generate_password_hash('admin'), 'mañana', 'Dirección'))
    conn.commit()
    conn.close()

crear_tablas()

# --- Rutas ---
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        carnet = request.form.get('carnet')
        contrasena = request.form.get('contrasena')
        if not carnet or not contrasena:
            flash('Debe completar ambos campos', 'error')
            return redirect(url_for('login'))

        conn = get_db_connection()
        profesor = conn.execute('SELECT * FROM profesores WHERE carnet = ?', (carnet,)).fetchone()
        conn.close()

        if profesor and check_password_hash(profesor['contrasena'], contrasena):
            session.clear()
            session['user_name'] = profesor['nombre']
            if carnet == 'admin':
                session['user_role'] = 'admin'
                return redirect(url_for('dashboard_admin'))
            else:
                session['user_role'] = 'profesor'
                session['profesor_id'] = profesor['id']
                session['foto'] = profesor['foto'] if 'foto' in profesor.keys() else None
                return redirect(url_for('dashboard_profesor'))
        else:
            flash('Credenciales inválidas', 'error')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# --- ADMIN ---
@app.route('/dashboard_admin')
def dashboard_admin():
    if session.get('user_role') != 'admin':
        return redirect(url_for('login'))
    conn = get_db_connection()
    profesores = conn.execute('SELECT * FROM profesores').fetchall()
    licencias = conn.execute('''
        SELECT l.*, p.nombre FROM licencias l
        JOIN profesores p ON l.profesor_id = p.id
        ORDER BY l.fecha DESC
    ''').fetchall()
    conn.close()
    return render_template('dashboard_admin.html', profesores=profesores, licencias=licencias)

@app.route('/register_profesor', methods=['GET', 'POST'])
def register_profesor():
    if session.get('user_role') != 'admin':
        return redirect(url_for('login'))

    if request.method == 'POST':
        nombre = request.form.get('nombre')
        carnet = request.form.get('carnet')
        contrasena = request.form.get('contrasena')
        turno = request.form.get('turno')
        especialidad = request.form.get('especialidad')
        foto = request.files.get('foto')

        if not (nombre and carnet and contrasena and turno and especialidad):
            flash('Todos los campos son obligatorios', 'error')
            return redirect(url_for('register_profesor'))

        foto_filename = None
        if foto:
            foto_filename = secure_filename(foto.filename)
            foto.save(os.path.join(UPLOAD_FOLDER, foto_filename))

        hashed_password = generate_password_hash(contrasena)
        conn = get_db_connection()
        try:
            conn.execute('''
                INSERT INTO profesores (nombre, carnet, contrasena, turno, especialidad, foto)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (nombre, carnet, hashed_password, turno, especialidad, foto_filename))
            conn.commit()
            flash('Profesor registrado correctamente', 'success')
        except sqlite3.IntegrityError:
            flash('El carnet ya está registrado', 'error')
        conn.close()
    return render_template('register_profesor.html')

@app.route('/eliminar_profesor/<int:id>')
def eliminar_profesor(id):
    if session.get('user_role') != 'admin':
        return redirect(url_for('login'))
    conn = get_db_connection()
    conn.execute('DELETE FROM profesores WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('dashboard_admin'))

@app.route('/aceptar_licencia/<int:id>')
def aceptar_licencia(id):
    if session.get('user_role') != 'admin':
        return redirect(url_for('login'))
    conn = get_db_connection()
    conn.execute('UPDATE licencias SET estado = "Aceptada" WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('dashboard_admin'))

@app.route('/rechazar_licencia/<int:id>')
def rechazar_licencia(id):
    if session.get('user_role') != 'admin':
        return redirect(url_for('login'))
    conn = get_db_connection()
    conn.execute('UPDATE licencias SET estado = "Rechazada" WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('dashboard_admin'))


# Continuación de app.py

# --- PROFESOR ---
@app.route('/dashboard_profesor')
def dashboard_profesor():
    if session.get('user_role') != 'profesor':
        return redirect(url_for('login'))
    conn = get_db_connection()
    licencias = conn.execute(
        'SELECT * FROM licencias WHERE profesor_id = ? ORDER BY fecha DESC',
        (session['profesor_id'],)
    ).fetchall()
    conn.close()
    return render_template('dashboard_profesor.html', licencias=licencias, foto=session.get('foto'))

@app.route('/solicitudes', methods=['GET', 'POST'])
def solicitudes():
    if session.get('user_role') != 'profesor':
        return redirect(url_for('login'))
    if request.method == 'POST':
        motivo = request.form.get('motivo')
        fecha_inicio = request.form.get('fecha_inicio')
        fecha_fin = request.form.get('fecha_fin')
        archivo = request.files.get('archivo')

        if not motivo or not fecha_inicio or not fecha_fin:
            flash('Todos los campos son obligatorios', 'error')
            return redirect(url_for('solicitudes'))

        try:
            inicio_dt = datetime.strptime(fecha_inicio, "%Y-%m-%d")
            fin_dt = datetime.strptime(fecha_fin, "%Y-%m-%d")
            if inicio_dt > fin_dt:
                flash('La fecha de inicio no puede ser posterior a la fecha de fin', 'error')
                return redirect(url_for('solicitudes'))
            if inicio_dt < datetime.now():
                flash('No puedes solicitar fechas pasadas', 'error')
                return redirect(url_for('solicitudes'))
        except ValueError:
            flash('Formato de fecha inválido', 'error')
            return redirect(url_for('solicitudes'))

        fecha_solicitud = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        archivo_nombre = None
        if archivo:
            archivo_nombre = secure_filename(archivo.filename)
            archivo.save(os.path.join(COMPROBANTES_FOLDER, archivo_nombre))

        conn = get_db_connection()
        conn.execute('''
            INSERT INTO licencias (profesor_id, fecha, motivo, estado, fecha_inicio, fecha_fin, archivo)
            VALUES (?, ?, ?, 'En espera', ?, ?, ?)
        ''', (session['profesor_id'], fecha_solicitud, motivo, fecha_inicio, fecha_fin, archivo_nombre))
        conn.commit()
        conn.close()
        flash('Solicitud enviada correctamente', 'success')
        return redirect(url_for('dashboard_profesor'))
    current_date = datetime.now().strftime('%Y-%m-%d')
    return render_template('solicitudes.html', current_date=current_date)

@app.route('/cambiar_contrasena', methods=['GET', 'POST'])
def cambiar_contrasena():
    if session.get('user_role') != 'profesor':
        return redirect(url_for('login'))

    if request.method == 'POST':
        actual = request.form.get('actual')
        nueva = request.form.get('nueva')
        repetir = request.form.get('repetir')

        if not actual or not nueva or not repetir:
            flash('Todos los campos son obligatorios', 'error')
            return redirect(url_for('cambiar_contrasena'))

        if nueva != repetir:
            flash('Las nuevas contraseñas no coinciden', 'error')
            return redirect(url_for('cambiar_contrasena'))

        conn = get_db_connection()
        profesor = conn.execute('SELECT * FROM profesores WHERE id = ?', (session['profesor_id'],)).fetchone()

        if not check_password_hash(profesor['contrasena'], actual):
            flash('La contraseña actual es incorrecta', 'error')
            conn.close()
            return redirect(url_for('cambiar_contrasena'))

        nueva_hash = generate_password_hash(nueva)
        conn.execute('UPDATE profesores SET contrasena = ? WHERE id = ?', (nueva_hash, session['profesor_id']))
        conn.commit()
        conn.close()

        flash('Contraseña actualizada correctamente', 'success')
        return redirect(url_for('dashboard_profesor'))

    return render_template('cambiar_contrasena.html')

@app.route('/editar_profesor/<int:id>', methods=['GET', 'POST'])
def editar_profesor(id):
    if session.get('user_role') != 'admin':
        return redirect(url_for('login'))

    conn = get_db_connection()
    profesor = conn.execute('SELECT * FROM profesores WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        nombre = request.form.get('nombre')
        carnet = request.form.get('carnet')
        turno = request.form.get('turno')
        especialidad = request.form.get('especialidad')
        foto = request.files.get('foto')

        if not (nombre and carnet and turno and especialidad):
            flash('Todos los campos son obligatorios', 'error')
            return redirect(url_for('editar_profesor', id=id))

        foto_filename = profesor['foto']
        if foto and foto.filename:
            foto_filename = secure_filename(foto.filename)
            foto.save(os.path.join(UPLOAD_FOLDER, foto_filename))

        try:
            conn.execute('''
                UPDATE profesores SET nombre = ?, carnet = ?, turno = ?, especialidad = ?, foto = ? WHERE id = ?
            ''', (nombre, carnet, turno, especialidad, foto_filename, id))
            conn.commit()
            flash('Datos actualizados correctamente', 'success')
            return redirect(url_for('dashboard_admin'))
        except sqlite3.IntegrityError:
            flash('El carnet ya está en uso por otro profesor', 'error')
            return redirect(url_for('editar_profesor', id=id))

    return render_template('editar_profesor.html', profesor=profesor)

if __name__ == '__main__':
    app.run(debug=True)
