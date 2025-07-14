from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import os

app = FastAPI()

# Configura CORS para permitir todas las conexiones (puedes restringirlo si lo necesitas)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo de entrada
class ChatRequest(BaseModel):
    message: str

# Cliente de OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    completion = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Ets Planetaquim, un assistent que ajuda amb empatia i saviesa."},
            {"role": "user", "content": request.message}
        ]
    )
    return {"response": completion.choices[0].message.content.strip()}
