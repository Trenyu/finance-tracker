# database.py

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 1. Lee la variable de entorno que Render te da.
#    No necesitamos dotenv en producción.
DATABASE_URL = os.environ.get('DATABASE_URL')

# 2. (MUY RECOMENDADO) Render a veces usa "postgres://" y SQLAlchemy necesita "postgresql://"
#    Esta línea lo corrige automáticamente si es necesario.
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# 3. (MUY RECOMENDADO) Una comprobación para asegurarnos de que la URL existe.
if not DATABASE_URL:
    raise ValueError("Error: La variable de entorno DATABASE_URL no está configurada.")

# Crear el motor de SQLAlchemy con la URL correcta
engine = create_engine(DATABASE_URL)

# El resto de tu código se queda igual
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def init_db():
    # Se importa acá para evitar dependencias circulares
    from models import Gasto 
    Base.metadata.create_all(bind=engine)