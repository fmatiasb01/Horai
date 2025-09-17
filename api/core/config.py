import os

class Settings:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")  # Set this via environment variable
    GROQ_MODEL = "llama-3.1-8b-instant"

settings = Settings()