from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.chat import ChatQueryRequest, ChatQueryResponse, ChartConfig
from app.services.ai_service import AIService
from app.services.sql_executor import SQLExecutor, SQLExecutionError
from app.core.logging import logger

router = APIRouter()


@router.post("/query", response_model=ChatQueryResponse)
def handle_chat_query(body: ChatQueryRequest, db: Session = Depends(get_db)):
    question = body.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    logger.info(f"Processing chat query: '{question}'")

    try:
        # Step 1: Natural Language to SQL
        sql_query = AIService.generate_sql_query(question)

        # Step 2: Execute SQL Query
        query_result = SQLExecutor.execute_query(sql_query)

        # Step 3: Generate AI Business Insight
        insight = AIService.generate_business_insight(question, sql_query, query_result)

        # Step 4: Recommend Dynamic Chart Type
        chart_recommendation = AIService.recommend_chart_type(
            columns=query_result["columns"],
            rows=query_result["rows"]
        )

        return ChatQueryResponse(
            question=question,
            sql_query=sql_query,
            columns=query_result["columns"],
            rows=query_result["rows"],
            row_count=query_result["row_count"],
            business_insight=insight,
            chart_config=ChartConfig(**chart_recommendation)
        )

    except SQLExecutionError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in chat query handler: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
