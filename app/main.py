## Точка входа
from fastapi import FastAPI
from app.routes import ping, auth

app = FastAPI()

app.include_router(ping.router)
app.include_router(auth.router)