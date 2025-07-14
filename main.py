
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import openai
import os

app = FastAPI()

# Configurar CORS para permitir solicitudes desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes restringir a tu dominio en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Establecer la clave de API de OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    message = data.get("message", "")

    if not message:
        return {"response": "No he recibido ningún mensaje."}

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Eres Planetaquim, un chatbot con la personalidad de Quim. Hablas con ética, calidez, humor y una mirada alternativa de curiosa perspectiva."},
                {"role": "user", "content": message}
            ]
        )
        reply = completion.choices[0].message.content
        return {"response": reply}

    except Exception as e:
        return {"response": f"Ocurrió un error: {str(e)}"}
