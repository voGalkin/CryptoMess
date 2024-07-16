from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from cryptography.fernet import Fernet

app = FastAPI()

# Генерация ключа
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Подключение статических файлов и шаблонов
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class Message(BaseModel):
    text: str

@app.get("/", response_class=HTMLResponse)
async def get(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/encrypt")
async def encrypt_message(message: Message):
    try:
        encrypted_text = cipher_suite.encrypt(message.text.encode())
        return {"encrypted_text": encrypted_text.decode()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/decrypt")
async def decrypt_message(message: Message):
    try:
        decrypted_text = cipher_suite.decrypt(message.text.encode())
        return {"decrypted_text": decrypted_text.decode()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
