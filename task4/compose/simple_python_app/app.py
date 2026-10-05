import os
from contextlib import asynccontextmanager, closing

import psycopg2
from fastapi import FastAPI
from pydantic import BaseModel, Field


def connect_db():
    return psycopg2.connect(
        host=os.getenv("API_DB_HOST", "127.0.0.1"),
        port=os.getenv("API_DB_PORT", "5432"),
        dbname=os.getenv("API_DB_NAME", "api"),
        user=os.getenv("API_DB_USER", "apiuser"),
        password=os.getenv("API_DB_PASS", "apipass"),
        connect_timeout=5,
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    with closing(connect_db()) as connection:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS notes (
                        id SERIAL PRIMARY KEY,
                        text TEXT NOT NULL
                    );
                """)
    yield


app = FastAPI(title="Lab 1 — Group 13", lifespan=lifespan)


class NoteCreate(BaseModel):
    text: str = Field(min_length=1, max_length=1000)


@app.get("/")
def root():
    with closing(connect_db()) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()[0]
    return {"message": "Hello World", "postgres_version": version}


@app.get("/hello/{name}")
def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.post("/notes", status_code=201)
def create_note(note: NoteCreate):
    with closing(connect_db()) as connection:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO notes (text) VALUES (%s) RETURNING id, text;",
                    (note.text,),
                )
                row = cursor.fetchone()
    return {"id": row[0], "text": row[1]}


@app.get("/notes")
def list_notes():
    with closing(connect_db()) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, text FROM notes ORDER BY id;")
            rows = cursor.fetchall()
    return [{"id": row[0], "text": row[1]} for row in rows]

# Cache test for v2

# Cache test for v2
