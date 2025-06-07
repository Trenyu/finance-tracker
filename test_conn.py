from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()  # Carga las variables del .env

DATABASE_URL = os.getenv("DATABASE_URL")

print(f"Intentando conectar a: {DATABASE_URL}")

try:
    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        print("✅ ¡Conexión exitosa!")
except Exception as e:
    print("❌ Falló la conexión.")
    print(e)
