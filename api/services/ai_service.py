from groq import Groq
from ..core.config import settings

class AIService:
    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY)
    
    def generate_response(self, mensaje_usuario: str) -> str:
        print(f"Intentando generar respuesta para mensaje: {mensaje_usuario[:50]}...")
        print(f"API Key configurada: {self.client.api_key[:8]}...")
        print(f"Modelo configurado: {settings.GROQ_MODEL}")
        
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "Eres HORAI, un asistente amigable que ayuda con productividad y organización personal."
                    },
                    {
                        "role": "user", 
                        "content": mensaje_usuario
                    }
                ],
                model=settings.GROQ_MODEL,
                max_tokens=500,
                temperature=0.7,
            )
            
            if not chat_completion or not chat_completion.choices:
                raise ValueError("La respuesta de GROQ está vacía")
                
            print("Respuesta generada exitosamente")
            return chat_completion.choices[0].message.content
            
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"Error generando respuesta: {str(e)}")
            print(f"Detalles del error:\n{error_details}")
            raise Exception(f"Error al generar respuesta con GROQ: {str(e)}")

# Instancia global
ai_service = AIService()