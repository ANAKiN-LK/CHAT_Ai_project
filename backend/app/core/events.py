from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.config import settings
@asynccontextmanager
async def lifespan(app: FastAPI):
    yield