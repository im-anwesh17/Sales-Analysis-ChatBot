from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.analytics_service import AnalyticsService

router = APIRouter()


@router.get("/rfm")
def get_rfm_analytics(db: Session = Depends(get_db)):
    return AnalyticsService.calculate_rfm_segmentation(db)
