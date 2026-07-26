import re
import pandas as pd
from typing import Dict, Any, List, Tuple
from sqlalchemy import text
from app.db.session import engine
from app.core.logging import logger

FORBIDDEN_KEYWORDS = [
    r"\bDROP\b", r"\bDELETE\b", r"\bUPDATE\b", r"\bINSERT\b",
    r"\bALTER\b", r"\bCREATE\b", r"\bTRUNCATE\b", r"\bGRANT\b",
    r"\bREVOKE\b", r"\bEXEC\b", r"\bEXECUTE\b"
]


class SQLExecutionError(Exception):
    pass


class SQLExecutor:
    @staticmethod
    def validate_sql(sql_query: str) -> Tuple[bool, str]:
        """
        Validates that the provided SQL query is strictly a read-only SELECT statement.
        """
        cleaned_sql = sql_query.strip().strip(";").strip()
        
        if not cleaned_sql:
            return False, "Empty SQL query."

        # Check for multi-statement execution (semicolons inside statement)
        if ";" in cleaned_sql:
            return False, "Multi-statement SQL queries are strictly prohibited."

        # Ensure query starts with SELECT or WITH (CTE)
        upper_sql = cleaned_sql.upper()
        if not (upper_sql.startswith("SELECT") or upper_sql.startswith("WITH")):
            return False, "Only read-only SELECT or WITH (CTE) queries are permitted."

        # Check for forbidden mutation keywords
        for keyword in FORBIDDEN_KEYWORDS:
            if re.search(keyword, upper_sql):
                return False, f"Forbidden SQL keyword detected matching pattern '{keyword}'."

        return True, "Valid SELECT query."

    @classmethod
    def execute_query(cls, sql_query: str, limit: int = 100) -> Dict[str, Any]:
        """
        Executes a validated SELECT SQL query and returns column names, rows, and metadata.
        """
        is_valid, msg = cls.validate_sql(sql_query)
        if not is_valid:
            logger.warning(f"SQL Validation failed for query: {sql_query}. Reason: {msg}")
            raise SQLExecutionError(f"Security validation failed: {msg}")

        cleaned_sql = sql_query.strip().strip(";")
        
        # Apply safety LIMIT if not already present
        if "LIMIT" not in cleaned_sql.upper():
            cleaned_sql = f"{cleaned_sql} LIMIT {limit}"

        logger.info(f"Executing SQL Query: {cleaned_sql}")

        try:
            with engine.connect() as conn:
                df = pd.read_sql_query(text(cleaned_sql), conn)
            
            # Format datetime columns to ISO string
            for col in df.columns:
                if pd.api.types.is_datetime64_any_dtype(df[col]):
                    df[col] = df[col].dt.strftime('%Y-%m-%d %H:%M:%S')

            # Fill NaN values with None for clean JSON serialization
            df = df.where(pd.notnull(df), None)

            columns = list(df.columns)
            rows = df.to_dict(orient="records")
            row_count = len(rows)

            return {
                "success": True,
                "sql_query": cleaned_sql,
                "columns": columns,
                "rows": rows,
                "row_count": row_count
            }

        except Exception as e:
            logger.error(f"SQL execution error: {str(e)}")
            raise SQLExecutionError(f"Database Query Error: {str(e)}")
