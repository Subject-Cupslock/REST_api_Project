## Точка входа
from fastapi import FastAPI
from app.routes import ping

app = FastAPI()

app.include_router(ping.router)