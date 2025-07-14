from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
import os

# Configura tu clave API de OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")  # o ponla directamente como string, si estás en entorno de prueba

app = FastAPI()

# Permitir CORS (necesario para que funcione con el frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes restringir esto a ["https://planetaquim.netlify.app"] si quieres más seguridad
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Esquema del cuerpo de la petición
class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # o "gpt-3.5-turbo"
            messages=[
                {"role": "system", "content": "Eres un asistente cálido y amable llamado Planetaquim."},
                {"role": "user", "content": request.message}
            ]
        )
        answer = response.choices[0].message["content"].strip()
        return {"response": answer}

    except Exception as e:
        return {"error": str(e)}
