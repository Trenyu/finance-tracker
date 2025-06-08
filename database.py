from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os
DATABASE_URL = os.environ.get("DATABASE_URL")


# Cargar variables desde .env
load_dotenv()

# Obtener la URL de conexión desde la variable de entorno
DATABASE_URL = os.getenv("DATABASE_URL")

# Crear el motor de SQLAlchemy
engine = create_engine(DATABASE_URL)

# Base para declarar modelos
Base = declarative_base()

# Crear sesión para interactuar con la base
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Función para inicializar la base (crear tablas)
def init_db():
    import models  # se importa acá para evitar dependencias circulares
    Base.metadata.create_all(bind=engine)
