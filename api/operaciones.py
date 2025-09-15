from .modelos import Conversacion
from sqlalchemy.orm import Session
from sqlalchemy import desc

def crear_conversacion(db: Session, mensaje_usuario: str, respuesta_bot: str, sesion_id: str = None):
    if not sesion_id:
        import uuid
        sesion_id = str(uuid.uuid4())
    
    conversacion = Conversacion(
        mensaje_usuario=mensaje_usuario, 
        respuesta_bot=respuesta_bot,
        sesion_id=sesion_id
    )
    db.add(conversacion)
    db.commit()
    db.refresh(conversacion)
    return conversacion

def obtener_conversaciones_por_sesion(db: Session, sesion_id: str):
    return db.query(Conversacion).filter(
        Conversacion.sesion_id == sesion_id
    ).order_by(Conversacion.fecha.asc()).all()

def obtener_todas_las_conversaciones(db: Session):
    return db.query(Conversacion).order_by(Conversacion.fecha.desc()).all()

def eliminar_conversacion(db: Session, conversacion_id: int):
    conversacion = db.query(Conversacion).filter(Conversacion.id == conversacion_id).first()
    if conversacion:
        db.delete(conversacion)
        db.commit()
        return True
    return False

def eliminar_sesion_completa(db: Session, sesion_id: str):
    conversaciones = db.query(Conversacion).filter(Conversacion.sesion_id == sesion_id).all()
    for conversacion in conversaciones:
        db.delete(conversacion)
    db.commit()
    return len(conversaciones)

def eliminar_todas_las_conversaciones(db: Session):
    count = db.query(Conversacion).count()
    db.query(Conversacion).delete()
    db.commit()
    return count