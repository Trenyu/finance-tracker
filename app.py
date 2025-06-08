# app.py

from flask import Flask, render_template, request, redirect
# Asegúrate de importar 'engine' desde tu archivo de base de datos
from database import SessionLocal, init_db, engine
from models import Gasto
from datetime import datetime
# Importa la función 'inspect' de SQLAlchemy
from sqlalchemy import inspect

# Crea la aplicación Flask
app = Flask(__name__)

# --- INICIO DEL CÓDIGO MÁGICO ---
# Este bloque se asegura de que las tablas existan antes de que la app empiece a funcionar
with app.app_context():
    inspector = inspect(engine)
    if not inspector.has_table("gastos"):
        print(">>> La tabla 'gastos' no existe. Creándola ahora...")
        init_db()
        print(">>> Tabla 'gastos' creada con éxito.")
# --- FIN DEL CÓDIGO MÁGICO ---


PRESUPUESTO_FILE = 'presupuesto.txt'

def guardar_presupuesto(valor):
    with open(PRESUPUESTO_FILE, 'w') as f:
        f.write(str(valor))

def cargar_presupuesto():
    try:
        with open(PRESUPUESTO_FILE, 'r') as f:
            return float(f.read())
    except (FileNotFoundError, ValueError):
        return None

@app.route('/set_presupuesto', methods=['POST'])
def set_presupuesto():
    presupuesto = float(request.form['presupuesto'])
    guardar_presupuesto(presupuesto)
    return redirect('/')

@app.route('/')
def index():
    presupuesto_maximo = cargar_presupuesto()
    db = SessionLocal()
    gastos = db.query(Gasto).all()
    db.close()

    total_gastos = sum(g.monto for g in gastos)
    
    restante = None
    aviso = None
    if presupuesto_maximo is not None:
        restante = presupuesto_maximo - total_gastos
        if restante < 0:
            aviso = f"Atención: Has superado tu presupuesto de ${presupuesto_maximo:.2f}!"

    categorias = list(set(g.categoria for g in gastos))

    return render_template(
        'index.html', 
        gastos=gastos, 
        total=total_gastos, 
        categorias=categorias, 
        presupuesto_maximo=presupuesto_maximo,
        restante=restante,
        aviso=aviso
    )

# ... (El resto de tus rutas como '/agregar', '/filtrar', etc., se quedan igual) ...
# Asegúrate de que todas tus otras rutas están aquí.

@app.route('/agregar', methods=['POST'])
def agregar():
    fecha_str = request.form['fecha']
    categoria = request.form['categoria']
    descripcion = request.form['descripcion']
    monto = float(request.form['monto'])
    fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
    
    db = SessionLocal()
    nuevo_gasto = Gasto(fecha=fecha, categoria=categoria, descripcion=descripcion, monto=monto)
    db.add(nuevo_gasto)
    db.commit()
    db.close()
    return redirect('/')

@app.route('/filtrar', methods=['POST'])
def filtrar():
    categoria = request.form['categoria']
    db = SessionLocal()
    if categoria == "todos":
        gastos = db.query(Gasto).all()
    else:
        gastos = db.query(Gasto).filter(Gasto.categoria == categoria).all()
    db.close()

    total = sum(g.monto for g in gastos)
    categorias = list(set(g.categoria for g in gastos))
    
    return render_template('index.html', gastos=gastos, total=total, categorias=categorias)

@app.route('/reiniciar', methods=['POST'])
def reiniciar():
    db = SessionLocal()
    db.query(Gasto).delete()
    db.commit()
    db.close()
    return redirect('/')
    
# (Añade cualquier otra ruta que te falte)

if __name__ == '__main__':
    app.run(debug=True)