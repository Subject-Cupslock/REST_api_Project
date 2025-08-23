## Точка входа
from fastapi import FastAPI
from app.routes import ping, auth, items
from app.exceptions import (
    UserAlreadyExistsException, user_exists_handler,
    UserNotFoundException, user_not_found_handler,
    InvalidCredentialsException, invalid_credentials_handler,
    ItemNotFoundException, item_not_found_handler
)

app = FastAPI()

app.include_router(ping.router) ## /ping
app.include_router(auth.router) ## /docs 
app.include_router(items.router) ## items


app.add_exception_handler(UserAlreadyExistsException, user_exists_handler)
app.add_exception_handler(UserNotFoundException, user_not_found_handler)
app.add_exception_handler(InvalidCredentialsException, invalid_credentials_handler)
app.add_exception_handler(ItemNotFoundException, item_not_found_handler)
