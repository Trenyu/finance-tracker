from flask import Flask, render_template, request, redirect, send_file
from sqlalchemy.orm import Session
from database import SessionLocal, init_db
from models import Gasto
from datetime import datetime
import pandas as pd
import os

app = Flask(__name__)
init_db()
PRESUPUESTO_FILE = 'presupuesto.txt'

# Presupuesto

def guardar_presupuesto(valor):
    with open(PRESUPUESTO_FILE, 'w') as f:
        f.write(str(valor))

def cargar_presupuesto():
    if os.path.exists(PRESUPUESTO_FILE):
        with open(PRESUPUESTO_FILE) as f:
            return float(f.read())
    return None

@app.route('/presupuesto', methods=['POST'])
def presupuesto():
    nuevo_presupuesto = float(request.form['presupuesto'])
    guardar_presupuesto(nuevo_presupuesto)
    return redirect('/')

# Página principal
@app.route('/')
def index():
    db = SessionLocal()
    gastos = db.query(Gasto).all()
    db.close()

    presupuesto_maximo = cargar_presupuesto()
    total = sum(g.monto for g in gastos)
    restante = presupuesto_maximo - total if presupuesto_maximo else None

    aviso = None
    if presupuesto_maximo and total > presupuesto_maximo:
        aviso = f"⚠️ Atención: Has superado tu presupuesto de ${presupuesto_maximo}"

    categorias = list(set(g.categoria for g in gastos))

    return render_template(
        'index.html',
        gastos=gastos,
        total=total,
        categorias=categorias,
        aviso=aviso,
        presupuesto_maximo=presupuesto_maximo,
        restante=restante
    )

# Agregar gasto
@app.route('/agregar', methods=['POST'])
def agregar():
    fecha = datetime.strptime(request.form['fecha'], '%Y-%m-%d').date()
    categoria = request.form['categoria']
    descripcion = request.form['descripcion']
    monto = float(request.form['monto'])

    db: Session = SessionLocal()
    nuevo_gasto = Gasto(
        fecha=fecha,
        categoria=categoria,
        descripcion=descripcion,
        monto=monto
    )
    db.add(nuevo_gasto)
    db.commit()
    db.close()

    return redirect('/')

# Filtrar por categoría
@app.route('/filtrar', methods=['POST'])
def filtrar():
    categoria = request.form['categoria']
    db = SessionLocal()
    gastos = db.query(Gasto).filter(Gasto.categoria == categoria).all()
    categorias = list(set(g.categoria for g in db.query(Gasto).all()))
    db.close()

    total = sum(g.monto for g in gastos)

    return render_template('index.html', gastos=gastos, total=total, categorias=categorias)

# Reiniciar gastos
@app.route('/reiniciar', methods=['POST'])
def reiniciar():
    db = SessionLocal()
    db.query(Gasto).delete()
    db.commit()
    db.close()
    return redirect('/')

# Exportar gastos a Excel
@app.route('/exportar')
def exportar():
    db = SessionLocal()
    gastos = db.query(Gasto).all()
    db.close()

    data = [{
        'Fecha': g.fecha.strftime('%Y-%m-%d'),
        'Categoria': g.categoria,
        'Descripcion': g.descripcion,
        'Monto': g.monto
    } for g in gastos]

    df = pd.DataFrame(data)
    excel_file = "gastos_exportados.xlsx"
    df.to_excel(excel_file, index=False)
    return send_file(excel_file, as_attachment=True)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

