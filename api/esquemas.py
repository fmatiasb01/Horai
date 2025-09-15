from pydantic import BaseModel
from datetime import datetime

class ConversacionCrear(BaseModel):
    mensaje_usuario: str

class ConversacionMostrar(BaseModel):
    id: int
    mensaje_usuario: str
    respuesta_bot: str
    fecha: datetime

    class Config:
        orm_mode = True