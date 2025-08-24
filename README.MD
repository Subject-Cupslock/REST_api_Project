# REST API Project (FastAPI)

Проект демонстрирует реализацию REST API с использованием **FastAPI**, **SQLAlchemy**, **JWT-аутентификации** и покрытием тестами (**pytest**).  
API поддерживает регистрацию, авторизацию пользователей и работу с пользовательскими `items` (создание, чтение, обновление, удаление).

## 📌 Возможности
- Регистрация и авторизация пользователей (JWT).
- CRUD-операции над `items` (каждый пользователь видит и управляет только своими).
- Глобальная обработка ошибок через кастомные исключения.
- Тестовое покрытие (`pytest` + `TestClient`).

## 🚀 Технологии
- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Pydantic](https://docs.pydantic.dev/)
- [PyJWT](https://pyjwt.readthedocs.io/)
- [pytest](https://docs.pytest.org/)

## ⚙️ Установка и запуск

### 1. Клонирование репозитория
```bash
git clone https://github.com/username/rest_api_project.git
cd rest_api_project
```

### 2. Создание виртуального окружения
```bash
python -m venv venv
source venv/bin/activate      # Linux / Mac
venv\Scripts\activate         # Windows (PowerShell)
```

### 3. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 4. Запуск сервера
```bash
uvicorn app.main:app --reload
```

API будет доступен по адресу:  
👉 [http://127.0.0.1:8000](http://127.0.0.1:8000)  

Документация (Swagger UI):  
👉 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)  

## 🧪 Тестирование
Запуск всех тестов:
```bash
pytest -v
```

## 🔑 Авторизация
- **Регистрация:** `POST /auth/register`  
- **Вход:** `POST /auth/login`  

После входа возвращается `access_token`, который нужно передавать в заголовке:
```http
Authorization: Bearer <token>
```

## 📚 Примеры API-запросов

### 🔹 Создание item
```http
POST /items/
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "My Item",
  "description": "Some description"
}
```

### 🔹 Получение всех своих items
```http
GET /items/
Authorization: Bearer <token>
```

### 🔹 Обновление item
```http
PUT /items/{item_id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "Updated",
  "description": "New description"
}
```

### 🔹 Удаление item
```http
DELETE /items/{item_id}
Authorization: Bearer <token>
```




