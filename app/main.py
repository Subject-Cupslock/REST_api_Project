## Точка входа
from fastapi import FastAPI
from app.routes import ping, auth, items

app = FastAPI()

app.include_router(ping.router) ## /ping
app.include_router(auth.router) ## /docs 
app.include_router(items.router) ## items