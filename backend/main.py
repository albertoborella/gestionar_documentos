from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import create_db_and_tables
from routers import documentos


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan, title="API - GESTIONAR DOCUMENTOS", version="1.0.0")

app.include_router(documentos.router)

