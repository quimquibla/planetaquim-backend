
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import openai
import os

app = FastAPI()

# Seguridad CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # o especificar tu dominio en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Clave privada (la protegerás en Render)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.post("/chat")
async def chat_endpoint(request: Request):
    data = await request.json()
    user_message = data.get("message", "")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Ets Planetaquim, un bot càlid, lúcid i molt personalitzat. Escrius en català o castellà segons l'usuari. Adapta't emocionalment a qui tens al davant. Sigues una versió amable, empàtica, propera i amb profunditat."},
                {"role": "user", "content": user_message}
            ]
        )
        reply = response.choices[0].message["content"]
        return {"reply": reply}
    except Exception as e:
        return {"reply": f"Error: {str(e)}"}
