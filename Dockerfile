FROM python:3.10-slim

WORKDIR /app

RUN pip install --no-cache-dir \
    "fastapi>=0.104.0" \
    "uvicorn[standard]>=0.24.0" \
    "sqlalchemy>=2.0.0" \
    "psycopg2-binary>=2.9.0" \
    "pydantic[email]>=2.0.0" \          
    "pydantic-settings>=2.0.0" \
    "pydantic-core>=2.0.0" \
    "python-jose[cryptography]>=3.3.0" \
    "passlib[bcrypt]>=1.7.0" \
    "python-multipart>=0.0.6"

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]