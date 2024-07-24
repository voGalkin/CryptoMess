from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from cryptography.fernet import Fernet, InvalidToken

app = FastAPI()

# Подключение статических файлов и шаблонов
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class Message(BaseModel):
    text: str
    key: str

@app.get("/", response_class=HTMLResponse)
async def get(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/generate_key", response_class=PlainTextResponse)
async def generate_key():
    return Fernet.generate_key().decode()

@app.post("/encrypt")
async def encrypt_message(message: Message):
    try:
        cipher_suite = Fernet(message.key.encode())
        encrypted_text = cipher_suite.encrypt(message.text.encode())
        return {"encrypted_text": encrypted_text.decode()}
    except (ValueError, InvalidToken) as e:
        raise HTTPException(status_code=400, detail="Invalid encryption key")

@app.post("/decrypt")
async def decrypt_message(message: Message):
    try:
        cipher_suite = Fernet(message.key.encode())
        decrypted_text = cipher_suite.decrypt(message.text.encode())
        return {"decrypted_text": decrypted_text.decode()}
    except (ValueError, InvalidToken) as e:
        raise HTTPException(status_code=400, detail="Invalid encryption key or text")
