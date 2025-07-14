from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
import os

app = FastAPI()

# Configuración CORS para permitir peticiones del frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominio
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cargar clave de API desde variables de entorno
openai.api_key = os.getenv("OPENAI_API_KEY")

class MessageRequest(BaseModel):
    message: str

# Diccionario de nombres conocidos
nombres_conocidos = {
    "eloiu": "Eloiu 🌟",
    "carles": "Carles 🎸",
    "jur": "Jur 💫",
    "edit": "Edit 🌱",
    "xavi": "Xavi 🧠",
    "delia": "Delia 🌺",
    "quim": "Quim 🌞"
}

@app.post("/chat")
async def chat_endpoint(request: MessageRequest):
    message = request.message.strip()

    # Buscar nombres conocidos
    nombre_detectado = None
    for nombre in nombres_conocidos:
        if nombre in message.lower():
            nombre_detectado = nombres_conocidos[nombre]
            break

    # Respuesta personalizada si se detecta un nombre
    if nombre_detectado:
        response_text = f"¡Hola {nombre_detectado}! Me alegra que estés aquí. Planetaquim te acompaña amb estima i llum ✨"
    else:
        # Llamada a la API de OpenAI si no se detecta nombre
        try:
            completion = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Eres Quim, un ser lúcido, empático y sabio. Responde con calidez, curiosidad y cercanía."},
                    {"role": "user", "content": message}
                ]
            )
            response_text = completion.choices[0].message.content.strip()
        except Exception as e:
            response_text = "Ho sento... alguna cosa no ha funcionat bé amb la connexió 🛠️"

    return { "response": response_text }