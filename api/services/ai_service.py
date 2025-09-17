from groq import Groq
from ..core.config import settings

class AIService:
    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY)
    
    def generate_response(self, mensaje_usuario: str) -> str:
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
            
            return chat_completion.choices[0].message.content
            
        except Exception as e:
            return f"Lo siento, hubo un error: {str(e)}"

# Instancia global
ai_service = AIService()