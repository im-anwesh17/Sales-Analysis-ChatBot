from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional


class ChatQueryRequest(BaseModel):
    question: str = Field(..., example="What were the top 5 selling products by revenue?")


class ChartConfig(BaseModel):
    chart_type: str  # "line", "bar", "pie", "metric", "none"
    x_key: Optional[str] = None
    y_keys: List[str] = []


class ChatQueryResponse(BaseModel):
    question: str
    sql_query: str
    columns: List[str]
    rows: List[Dict[str, Any]]
    row_count: int
    business_insight: str
    chart_config: ChartConfig
