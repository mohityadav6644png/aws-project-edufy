from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.config import settings
from app.shared.database.mongodb import (
    connect_to_mongodb,
    close_mongodb_connection,
    check_database_connection
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongodb()

    yield

    await close_mongodb_connection()


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Automated Study and Quiz Notification System",
    lifespan=lifespan
)


@app.get("/")
async def home():
    return {
        "message": "Welcome to EduNotify",
        "version": settings.APP_VERSION
    }


@app.get("/health")
async def health_check():
    db_status = await check_database_connection()

    if not db_status:
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "database": "disconnected"
            }
        )

    return {
        "status": "healthy",
        "database": "connected"
    }