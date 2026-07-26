from pydantic import BaseModel
from typing import List, Dict, Any, Optional


class DashboardOverviewResponse(BaseModel):
    total_revenue: float
    total_orders: int
    avg_order_value: float
    active_customers: int
    monthly_growth_percent: float


class MonthlyTrendResponse(BaseModel):
    month: str
    orders_count: int
    revenue: float


class CategoryPerformanceResponse(BaseModel):
    category: str
    total_orders: int
    units_sold: int
    total_revenue: float


class RegionalPerformanceResponse(BaseModel):
    state: str
    total_orders: int
    total_revenue: float


class TopProductResponse(BaseModel):
    product_name: str
    category: str
    subcategory: str
    total_units_sold: int
    total_revenue: float
