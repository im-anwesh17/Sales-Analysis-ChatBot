from fastapi import APIRouter
from app.api.v1 import health, dashboard, analytics, chat

api_router = APIRouter()

api_router.include_router(health.router, tags=["Health"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])
api_router.include_router(chat.router, prefix="/chat", tags=["Chat & Text-to-SQL"])
