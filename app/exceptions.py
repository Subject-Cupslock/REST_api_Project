from fastapi import Request, status
from fastapi.responses import JSONResponse

class UserAlreadyExistsException(Exception):
    def __init__(self, email: str):
        self.email = email


async def user_exists_handler(request: Request, exc: UserAlreadyExistsException):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            'error': 'UserAlreadyExists',
            'message': f'User with email {exc.email} already exists'
        },
    )


class UserNotFoundException(Exception):
    def __init__(self, email: str):
        self.email = email


async def user_not_found_handler(request: Request, exc: UserNotFoundException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            'error': 'UserNotFound',
            'message': f'User with email {exc.email} not found'
        },
    )


class InvalidCredentialsException(Exception):
    pass


async def invalid_credentials_handler(request: Request, exc: InvalidCredentialsException):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={
            'error': 'InvalidCredentials',
            'message': 'Invalid username or password'
        },
        headers={'WWW-Authenticate': 'Bearer'},
    )


class ItemNotFoundException(Exception):
    def __init__(self, item_id: int):
        self.item_id = item_id


async def item_not_found_handler(request: Request, exc: ItemNotFoundException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            'error': 'ItemNotFound',
            'message': f'Item with id {exc.item_id} not found'
        },
    )