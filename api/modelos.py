from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid

Base = declarative_base()

class Conversacion(Base):
    __tablename__ = "conversaciones"
    id = Column(Integer, primary_key=True, index=True)
    sesion_id = Column(String, nullable=False, default=lambda: str(uuid.uuid4()))
    mensaje_usuario = Column(String, nullable=False)
    respuesta_bot = Column(String, nullable=False)
    fecha = Column(DateTime, default=lambda: datetime.now())