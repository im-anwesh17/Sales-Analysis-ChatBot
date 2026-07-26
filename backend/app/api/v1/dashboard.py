from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.services.analytics_service import AnalyticsService
from app.schemas.dashboard import (
    DashboardOverviewResponse,
    MonthlyTrendResponse,
    CategoryPerformanceResponse,
    RegionalPerformanceResponse,
    TopProductResponse
)

router = APIRouter()


@router.get("/overview", response_model=DashboardOverviewResponse)
def get_overview(db: Session = Depends(get_db)):
    return AnalyticsService.get_dashboard_overview(db)


@router.get("/monthly-trend", response_model=List[MonthlyTrendResponse])
def get_monthly_trend(db: Session = Depends(get_db)):
    return AnalyticsService.get_monthly_sales_trend(db)


@router.get("/categories", response_model=List[CategoryPerformanceResponse])
def get_categories(db: Session = Depends(get_db)):
    return AnalyticsService.get_category_performance(db)


@router.get("/regional", response_model=List[RegionalPerformanceResponse])
def get_regional(limit: int = 10, db: Session = Depends(get_db)):
    return AnalyticsService.get_regional_performance(db, limit=limit)


@router.get("/top-products", response_model=List[TopProductResponse])
def get_top_products(limit: int = 10, db: Session = Depends(get_db)):
    return AnalyticsService.get_top_products(db, limit=limit)
