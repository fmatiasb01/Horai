from .modelos import Conversacion
from sqlalchemy.orm import Session
from sqlalchemy import desc
from .services.ai_service import ai_service
from .utils.markdown_processor import process_markdown

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

def crear_conversacion_con_ia(db: Session, mensaje_usuario: str, sesion_id: str = None):
    """Crear conversación usando IA de Groq"""
    if not sesion_id:
        import uuid
        sesion_id = str(uuid.uuid4())
    
    # Generar respuesta con IA
    respuesta_bot_raw = ai_service.generate_response(mensaje_usuario)
    
    # Procesar markdown para mejorar el formato
    respuesta_bot = process_markdown(respuesta_bot_raw)
    
    # Guardar conversación
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

def obtener_sesiones_agrupadas(db: Session):
    """Obtener conversaciones agrupadas por sesión"""
    from sqlalchemy import func
    
    # Obtener todas las conversaciones ordenadas por fecha
    conversaciones = db.query(Conversacion).order_by(Conversacion.fecha.desc()).all()
    
    # Agrupar por sesión
    sesiones = {}
    for conv in conversaciones:
        if conv.sesion_id not in sesiones:
            sesiones[conv.sesion_id] = {
                'sesion_id': conv.sesion_id,
                'conversaciones': [],
                'primera_fecha': conv.fecha,
                'ultima_fecha': conv.fecha,
                'total_mensajes': 0
            }
        
        sesiones[conv.sesion_id]['conversaciones'].append(conv)
        sesiones[conv.sesion_id]['total_mensajes'] += 1
        
        # Actualizar fechas
        if conv.fecha > sesiones[conv.sesion_id]['ultima_fecha']:
            sesiones[conv.sesion_id]['ultima_fecha'] = conv.fecha
        if conv.fecha < sesiones[conv.sesion_id]['primera_fecha']:
            sesiones[conv.sesion_id]['primera_fecha'] = conv.fecha
    
    # Convertir a lista y ordenar por última fecha
    sesiones_lista = list(sesiones.values())
    sesiones_lista.sort(key=lambda x: x['ultima_fecha'], reverse=True)
    
    return sesiones_lista