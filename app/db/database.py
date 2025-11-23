"""
Configuración de base de datos PostgreSQL
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import settings
from contextlib import contextmanager
from typing import Generator

# Crear engine de SQLAlchemy
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # Verificar conexión antes de usar
    pool_size=5,  # Tamaño del pool de conexiones
    max_overflow=10,  # Conexiones adicionales permitidas
    echo=settings.DEBUG,  # Log de SQL queries en modo debug
)

# Crear SessionLocal
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """
    Dependency para obtener sesión de base de datos
    
    Uso en FastAPI:
    ```python
    @app.get("/")
    def read_root(db: Session = Depends(get_db)):
        ...
    ```
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def get_db_context():
    """
    Context manager para usar base de datos fuera de FastAPI
    
    Uso:
    ```python
    with get_db_context() as db:
        lead = db.query(Lead).first()
    ```
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Inicializar base de datos (crear tablas)"""
    from app.models.lead import Base
    Base.metadata.create_all(bind=engine)
    print("✅ Base de datos inicializada correctamente")


def drop_db():
    """Eliminar todas las tablas (usar con precaución)"""
    from app.models.lead import Base
    Base.metadata.drop_all(bind=engine)
    print("⚠️ Todas las tablas han sido eliminadas")
