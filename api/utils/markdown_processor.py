import markdown
import re

def process_markdown(text):
    """Convierte markdown a HTML y mejora el formato"""
    
    # Configurar markdown con extensiones
    md = markdown.Markdown(extensions=[
        'markdown.extensions.nl2br',
        'markdown.extensions.fenced_code',
        'markdown.extensions.tables',
    ])
    
    # Convertir a HTML
    html = md.convert(text)
    
    # Limpiar y mejorar el HTML
    html = improve_html_format(html)
    
    return html

def improve_html_format(html):
    """Mejora el formato HTML para que se vea mejor"""
    
    # Reemplazar listas con clases CSS personalizadas
    html = re.sub(r'<ul>', '<ul class="horai-list">', html)
    html = re.sub(r'<ol>', '<ol class="horai-list-numbered">', html)
    
    # Reemplazar párrafos con clases
    html = re.sub(r'<p>', '<p class="horai-paragraph">', html)
    
    # Reemplazar títulos con clases
    html = re.sub(r'<h2>', '<h2 class="horai-title">', html)
    html = re.sub(r'<h3>', '<h3 class="horai-subtitle">', html)
    
    # Reemplazar texto en negrita
    html = re.sub(r'<strong>', '<strong class="horai-bold">', html)
    
    # Reemplazar código
    html = re.sub(r'<code>', '<code class="horai-code">', html)
    
    return html