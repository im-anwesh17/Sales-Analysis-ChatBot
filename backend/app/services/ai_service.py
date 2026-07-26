import re
import json
from typing import Dict, Any, List, Optional
import google.generativeai as genai
import openai

from app.core.config import settings
from app.core.logging import logger
from app.services.sql_executor import SQLExecutor

DATABASE_SCHEMA_PROMPT = """
You are an expert SQL Data Analyst and Data Engineer specializing in Sales & E-commerce analytics.
Translate natural language questions into executable SQL queries.

### DATABASE SCHEMA & RULES:
1. Table `customers`:
   - customer_id (INTEGER PRIMARY KEY)
   - first_name (VARCHAR)
   - last_name (VARCHAR)
   - email (VARCHAR)
   - city (VARCHAR)
   - state (VARCHAR)
   - country (VARCHAR)
   - segment (VARCHAR) -> Options: 'Consumer', 'Corporate', 'Home Office'
   - created_at (TIMESTAMP)

2. Table `products`:
   - product_id (INTEGER PRIMARY KEY)
   - product_name (VARCHAR)
   - category (VARCHAR) -> Options: 'Electronics', 'Clothing', 'Home & Kitchen', 'Accessories'
   - subcategory (VARCHAR)
   - unit_price (FLOAT)
   - cost_price (FLOAT)
   - sku (VARCHAR)
   - is_active (BOOLEAN)

3. Table `orders`:
   - order_id (INTEGER PRIMARY KEY)
   - customer_id (INTEGER FK -> customers.customer_id)
   - order_date (TIMESTAMP)
   - shipping_city (VARCHAR)
   - shipping_state (VARCHAR)
   - status (VARCHAR) -> Options: 'Completed', 'Pending', 'Cancelled', 'Returned'
   - payment_method (VARCHAR)
   - total_amount (FLOAT)

4. Table `order_items`:
   - item_id (INTEGER PRIMARY KEY)
   - order_id (INTEGER FK -> orders.order_id)
   - product_id (INTEGER FK -> products.product_id)
   - quantity (INTEGER)
   - unit_price (FLOAT)
   - discount (FLOAT)
   - total_amount (FLOAT)

### SQL GENERATION RULES:
- ONLY output a valid SELECT or WITH (CTE) query. Do NOT include markdown formatting or extra text.
- Filter completed orders using `orders.status = 'Completed'` unless explicitly asked for returned/cancelled orders.
- Calculate revenue using `SUM(orders.total_amount)` or `SUM(order_items.total_amount)`.
- Use ANSI standard SQL functions. For date grouping, use `strftime('%Y-%m', order_date)` or `DATE_TRUNC('month', order_date)`.
- Order results by the primary metric DESC (e.g. revenue, order_count).
- Always include a reasonable LIMIT (e.g., LIMIT 10 for top lists, LIMIT 100 max).
"""


class AIService:
    @staticmethod
    def _clean_sql_output(raw_text: str) -> str:
        """Removes markdown code blocks (```sql ... ```) and whitespace."""
        cleaned = raw_text.strip()
        cleaned = re.sub(r"^```sql\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"^```\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)
        return cleaned.strip()

    @classmethod
    def generate_sql_query(cls, user_question: str) -> str:
        """Generates SQL query from Natural Language question."""
        logger.info(f"Generating SQL query for user question: {user_question}")
        
        # 1. Check AI Provider
        if settings.AI_PROVIDER == "gemini" and settings.GEMINI_API_KEY:
            try:
                genai.configure(api_key=settings.GEMINI_API_KEY)
                model = genai.GenerativeModel(settings.GEMINI_MODEL)
                prompt = f"{DATABASE_SCHEMA_PROMPT}\nUser Question: {user_question}\nGenerate SQL:"
                response = model.generate_content(prompt)
                return cls._clean_sql_output(response.text)
            except Exception as e:
                logger.error(f"Gemini API error during SQL generation: {str(e)}")

        elif settings.AI_PROVIDER == "openai" and settings.OPENAI_API_KEY:
            try:
                client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
                response = client.chat.completions.create(
                    model=settings.OPENAI_MODEL,
                    messages=[
                        {"role": "system", "content": DATABASE_SCHEMA_PROMPT},
                        {"role": "user", "content": f"Generate SQL query for: {user_question}"}
                    ],
                    temperature=0.0
                )
                return cls._clean_sql_output(response.choices[0].message.content)
            except Exception as e:
                logger.error(f"OpenAI API error during SQL generation: {str(e)}")

        # Heuristic Rule-Based Fallback Engine if AI API keys are not provided or error occurs
        logger.info("Using Fallback Heuristic SQL Engine.")
        return cls._fallback_sql_generator(user_question)

    @classmethod
    def _fallback_sql_generator(cls, q: str) -> str:
        q_lower = q.lower()
        if "top" in q_lower and "product" in q_lower:
            return """SELECT p.product_name, p.category, SUM(oi.quantity) as units_sold, ROUND(SUM(oi.total_amount), 2) as total_revenue
FROM products p
JOIN order_items oi ON p.product_id = oi.product_id
JOIN orders o ON o.order_id = oi.order_id
WHERE o.status = 'Completed'
GROUP BY p.product_id, p.product_name, p.category
ORDER BY total_revenue DESC
LIMIT 10;"""

        elif "region" in q_lower or "state" in q_lower or "city" in q_lower:
            return """SELECT o.shipping_state as state, COUNT(DISTINCT o.order_id) as total_orders, ROUND(SUM(o.total_amount), 2) as revenue
FROM orders o
WHERE o.status = 'Completed'
GROUP BY o.shipping_state
ORDER BY revenue DESC
LIMIT 10;"""

        elif "monthly" in q_lower or "trend" in q_lower or "revenue over time" in q_lower:
            return """SELECT strftime('%Y-%m', o.order_date) as month, COUNT(DISTINCT o.order_id) as total_orders, ROUND(SUM(o.total_amount), 2) as monthly_revenue
FROM orders o
WHERE o.status = 'Completed'
GROUP BY month
ORDER BY month ASC;"""

        elif "customer" in q_lower and ("top" in q_lower or "best" in q_lower or "highest" in q_lower):
            return """SELECT c.first_name || ' ' || c.last_name as customer_name, c.email, c.segment, COUNT(DISTINCT o.order_id) as total_orders, ROUND(SUM(o.total_amount), 2) as total_spent
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE o.status = 'Completed'
GROUP BY c.customer_id, customer_name, c.email, c.segment
ORDER BY total_spent DESC
LIMIT 10;"""

        elif "category" in q_lower or "categories" in q_lower:
            return """SELECT p.category, COUNT(DISTINCT oi.order_id) as total_orders, ROUND(SUM(oi.total_amount), 2) as total_revenue
FROM products p
JOIN order_items oi ON p.product_id = oi.product_id
JOIN orders o ON o.order_id = oi.order_id
WHERE o.status = 'Completed'
GROUP BY p.category
ORDER BY total_revenue DESC;"""

        elif "declining" in q_lower or "returned" in q_lower or "cancel" in q_lower:
            return """SELECT o.status, COUNT(o.order_id) as order_count, ROUND(SUM(o.total_amount), 2) as total_value
FROM orders o
GROUP BY o.status
ORDER BY order_count DESC;"""

        else:
            # Default overview query
            return """SELECT strftime('%Y-%m', o.order_date) as month, ROUND(SUM(o.total_amount), 2) as revenue
FROM orders o
WHERE o.status = 'Completed'
GROUP BY month
ORDER BY month ASC
LIMIT 12;"""

    @classmethod
    def generate_business_insight(cls, user_question: str, sql_query: str, query_result: Dict[str, Any]) -> str:
        """Generates executive summary/insight based on SQL results."""
        rows = query_result.get("rows", [])
        if not rows:
            return "No data returned for this query parameter."

        # Truncate rows for prompt length safety
        sample_rows = rows[:10]
        
        prompt = f"""
Given the natural language question: "{user_question}"
SQL Query Executed: {sql_query}
Data Result (first {len(sample_rows)} rows):
{json.dumps(sample_rows, indent=2)}

Provide a concise 2-3 sentence executive business insight summarizing key takeaways, trends, or notable figures (e.g. top category, percentage share, highest revenue month/state). Keep it clear, professional, and data-backed.
"""
        if settings.AI_PROVIDER == "gemini" and settings.GEMINI_API_KEY:
            try:
                genai.configure(api_key=settings.GEMINI_API_KEY)
                model = genai.GenerativeModel(settings.GEMINI_MODEL)
                response = model.generate_content(prompt)
                return response.text.strip()
            except Exception as e:
                logger.error(f"Gemini API error during insight generation: {str(e)}")

        elif settings.AI_PROVIDER == "openai" and settings.OPENAI_API_KEY:
            try:
                client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
                response = client.chat.completions.create(
                    model=settings.OPENAI_MODEL,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3
                )
                return response.choices[0].message.content.strip()
            except Exception as e:
                logger.error(f"OpenAI API error during insight generation: {str(e)}")

        # Fallback automated insight synthesis
        return cls._fallback_insight_generator(rows, query_result.get("columns", []))

    @classmethod
    def _fallback_insight_generator(cls, rows: List[Dict[str, Any]], columns: List[str]) -> str:
        if not rows or not columns:
            return "Query completed successfully."

        first_row = rows[0]
        num_rows = len(rows)

        # Look for numeric metrics
        numeric_cols = [c for c in columns if isinstance(first_row.get(c), (int, float))]
        label_cols = [c for c in columns if c not in numeric_cols]

        if numeric_cols and label_cols:
            main_label_col = label_cols[0]
            main_num_col = numeric_cols[0]

            top_item = first_row.get(main_label_col, "N/A")
            top_val = first_row.get(main_num_col, 0)
            
            if isinstance(top_val, float):
                formatted_val = f"${top_val:,.2f}" if "revenue" in main_num_col or "spent" in main_num_col or "amount" in main_num_col else f"{top_val:,.2f}"
            else:
                formatted_val = f"{top_val:,}"

            return f"Analysis shows that '{top_item}' leads with {formatted_val} ({main_num_col.replace('_', ' ')}), representing the top performer across {num_rows} evaluated records."

        return f"Query returned {num_rows} records. The top entry is '{first_row.get(columns[0])}'."

    @classmethod
    def recommend_chart_type(cls, columns: List[str], rows: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Determines the optimal Recharts component type ('line', 'bar', 'pie', 'metric')
        and identifies dataKeys for X-axis and Y-axis/Series.
        """
        if not rows or not columns:
            return {"chart_type": "none", "x_key": None, "y_keys": []}

        if len(rows) == 1 and len(columns) == 1:
            return {"chart_type": "metric", "x_key": columns[0], "y_keys": [columns[0]]}

        first_row = rows[0]
        
        # Check column types
        date_cols = [c for c in columns if any(k in c.lower() for k in ["date", "month", "year", "time", "day", "quarter"])]
        numeric_cols = [c for c in columns if isinstance(first_row.get(c), (int, float))]
        category_cols = [c for c in columns if c not in numeric_cols and c not in date_cols]

        x_key = columns[0]
        y_keys = numeric_cols if numeric_cols else [columns[-1]]

        # Chart type selection heuristics
        if date_cols:
            x_key = date_cols[0]
            return {
                "chart_type": "line",
                "x_key": x_key,
                "y_keys": y_keys
            }
        
        if len(rows) <= 5 and len(numeric_cols) >= 1 and any(k in columns[0].lower() for k in ["category", "segment", "status", "payment"]):
            return {
                "chart_type": "pie",
                "x_key": columns[0],
                "y_keys": [y_keys[0]]
            }

        return {
            "chart_type": "bar",
            "x_key": x_key,
            "y_keys": y_keys
        }
