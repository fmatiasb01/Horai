from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Crear la conexión a la base de datos SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:////app/data/horai.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependencia para obtener la sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()