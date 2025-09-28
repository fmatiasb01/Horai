from fastapi import FastAPI, Depends, Request, Form, File, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from .core.db import engine, get_db
from .modelos import Base
from .operaciones import (
    crear_conversacion_con_ia,
    obtener_conversaciones_por_sesion, 
    obtener_todas_las_conversaciones,
    obtener_sesiones_agrupadas,
    eliminar_conversacion,
    eliminar_sesion_completa,
    eliminar_todas_las_conversaciones
)
from sqlalchemy.orm import Session
import uuid

Base.metadata.create_all(bind=engine)

app = FastAPI(title="HORAI Asistente")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def mostrar_chat(request: Request, sesion_id: str = None, db: Session = Depends(get_db)):
    if not sesion_id:
        # SIEMPRE crear una nueva sesión por defecto
        sesion_id = str(uuid.uuid4())
    
    conversaciones = obtener_conversaciones_por_sesion(db, sesion_id)
    
    return templates.TemplateResponse("chat.html", {
        "request": request, 
        "conversaciones": conversaciones,
        "sesion_id": sesion_id
    })

@app.get("/nuevo-chat", response_class=HTMLResponse)
def nuevo_chat(request: Request, db: Session = Depends(get_db)):
    nuevo_sesion_id = str(uuid.uuid4())
    
    return templates.TemplateResponse("chat.html", {
        "request": request, 
        "conversaciones": [],
        "sesion_id": nuevo_sesion_id
    })

@app.post("/enviar", response_class=HTMLResponse)
async def enviar_mensaje(request: Request, db: Session = Depends(get_db)):
    try:
        form = await request.form()
        mensaje_usuario = str(form.get("mensaje_usuario", "")).strip()
        sesion_id = str(form.get("sesion_id", "")).strip()
        
        if not mensaje_usuario:
            return RedirectResponse("/", status_code=303)
        
        if not sesion_id:
            sesion_id = str(uuid.uuid4())
        
        # Usar IA para generar respuesta
        crear_conversacion_con_ia(db, mensaje_usuario, sesion_id)
        return RedirectResponse(f"/?sesion_id={sesion_id}", status_code=303)
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Error en /enviar: {str(e)}\n{error_details}")
        return templates.TemplateResponse("chat.html", {
            "request": request,
            "error": f"Error: {str(e)}",
            "conversaciones": obtener_conversaciones_por_sesion(db, sesion_id) if sesion_id else [],
            "sesion_id": sesion_id
        })

@app.get("/login", response_class=HTMLResponse)
def mostrar_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/logout")
def logout():
    # Aquí iría la lógica para cerrar sesión (por ejemplo, limpiar cookies)
    return RedirectResponse("/", status_code=303)

# Ruta para inicio
@app.get("/inicio", response_class=HTMLResponse)
def mostrar_inicio(request: Request):
    return templates.TemplateResponse("inicio.html", {"request": request})


@app.get("/historial", response_class=HTMLResponse)
def mostrar_historial(request: Request, db: Session = Depends(get_db)):
    sesiones_agrupadas = obtener_sesiones_agrupadas(db)
    todas_conversaciones = obtener_todas_las_conversaciones(db)
    return templates.TemplateResponse("historial.html", {
        "request": request,
        "sesiones_agrupadas": sesiones_agrupadas,
        "todas_conversaciones": todas_conversaciones
    })

@app.post("/eliminar-conversacion/{conversacion_id}")
def eliminar_conversacion_endpoint(conversacion_id: int, db: Session = Depends(get_db)):
    eliminar_conversacion(db, conversacion_id)
    return RedirectResponse("/historial", status_code=303)

@app.post("/eliminar-sesion/{sesion_id}")
def eliminar_sesion_endpoint(sesion_id: str, db: Session = Depends(get_db)):
    eliminar_sesion_completa(db, sesion_id)
    return RedirectResponse("/historial", status_code=303)

@app.post("/eliminar-todo")
def eliminar_todo_endpoint(db: Session = Depends(get_db)):
    eliminar_todas_las_conversaciones(db)
    return RedirectResponse("/historial", status_code=303)

@app.get("/salud")
def salud():
    return {"estado": "ok"}