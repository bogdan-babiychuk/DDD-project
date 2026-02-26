from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.chat.handlers import router as chat_router
from lifespan import close_kafka, start_kafka

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await start_kafka()
    yield
    await close_kafka()

def create() -> FastAPI:
    app = FastAPI(
        title="Kafka Project",
        description="Асинхронный проект на FastAPI и Kafka",
        docs_url="/api/docs",
        lifespan=lifespan
    )
    
    # Настройка CORS для работы с фронтендом
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"],  # React dev server
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    app.include_router(router=chat_router, prefix="/chat")
    return app

