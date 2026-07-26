import pandas as pd
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.logging import logger


class AnalyticsService:

    @staticmethod
    def get_dashboard_overview(db: Session) -> Dict[str, Any]:
        """Calculates top-level KPI metrics for the executive dashboard."""
        sql_kpi = """
        SELECT 
            COUNT(DISTINCT o.order_id) as total_orders,
            COALESCE(SUM(o.total_amount), 0) as total_revenue,
            COALESCE(AVG(o.total_amount), 0) as avg_order_value,
            COUNT(DISTINCT o.customer_id) as active_customers
        FROM orders o
        WHERE o.status = 'Completed';
        """
        result = db.execute(text(sql_kpi)).mappings().first()
        
        # Monthly Growth Calculation
        sql_growth = """
        SELECT 
            strftime('%Y-%m', o.order_date) as month,
            SUM(o.total_amount) as monthly_revenue
        FROM orders o
        WHERE o.status = 'Completed'
        GROUP BY month
        ORDER BY month DESC
        LIMIT 2;
        """
        growth_rows = db.execute(text(sql_growth)).mappings().all()
        
        growth_rate = 0.0
        if len(growth_rows) >= 2:
            current_m = float(growth_rows[0]["monthly_revenue"] or 0)
            prev_m = float(growth_rows[1]["monthly_revenue"] or 0)
            if prev_m > 0:
                growth_rate = round(((current_m - prev_m) / prev_m) * 100, 2)

        return {
            "total_revenue": round(float(result["total_revenue"]), 2),
            "total_orders": int(result["total_orders"]),
            "avg_order_value": round(float(result["avg_order_value"]), 2),
            "active_customers": int(result["active_customers"]),
            "monthly_growth_percent": growth_rate
        }

    @staticmethod
    def get_monthly_sales_trend(db: Session) -> List[Dict[str, Any]]:
        """Returns monthly revenue and order volume time-series data."""
        sql = """
        SELECT 
            strftime('%Y-%m', o.order_date) as month,
            COUNT(DISTINCT o.order_id) as orders_count,
            ROUND(SUM(o.total_amount), 2) as revenue
        FROM orders o
        WHERE o.status = 'Completed'
        GROUP BY month
        ORDER BY month ASC;
        """
        rows = db.execute(text(sql)).mappings().all()
        return [dict(row) for row in rows]

    @staticmethod
    def get_category_performance(db: Session) -> List[Dict[str, Any]]:
        """Returns sales breakdown by product category."""
        sql = """
        SELECT 
            p.category,
            COUNT(DISTINCT oi.order_id) as total_orders,
            SUM(oi.quantity) as units_sold,
            ROUND(SUM(oi.total_amount), 2) as total_revenue
        FROM products p
        JOIN order_items oi ON p.product_id = oi.product_id
        JOIN orders o ON o.order_id = oi.order_id
        WHERE o.status = 'Completed'
        GROUP BY p.category
        ORDER BY total_revenue DESC;
        """
        rows = db.execute(text(sql)).mappings().all()
        return [dict(row) for row in rows]

    @staticmethod
    def get_regional_performance(db: Session, limit: int = 10) -> List[Dict[str, Any]]:
        """Returns top states/regions by total revenue."""
        sql = f"""
        SELECT 
            o.shipping_state as state,
            COUNT(DISTINCT o.order_id) as total_orders,
            ROUND(SUM(o.total_amount), 2) as total_revenue
        FROM orders o
        WHERE o.status = 'Completed'
        GROUP BY o.shipping_state
        ORDER BY total_revenue DESC
        LIMIT {limit};
        """
        rows = db.execute(text(sql)).mappings().all()
        return [dict(row) for row in rows]

    @staticmethod
    def get_top_products(db: Session, limit: int = 10) -> List[Dict[str, Any]]:
        """Returns top performing products by total revenue."""
        sql = f"""
        SELECT 
            p.product_name,
            p.category,
            p.subcategory,
            SUM(oi.quantity) as total_units_sold,
            ROUND(SUM(oi.total_amount), 2) as total_revenue
        FROM products p
        JOIN order_items oi ON p.product_id = oi.product_id
        JOIN orders o ON o.order_id = oi.order_id
        WHERE o.status = 'Completed'
        GROUP BY p.product_id, p.product_name, p.category, p.subcategory
        ORDER BY total_revenue DESC
        LIMIT {limit};
        """
        rows = db.execute(text(sql)).mappings().all()
        return [dict(row) for row in rows]

    @staticmethod
    def calculate_rfm_segmentation(db: Session) -> Dict[str, Any]:
        """
        Computes RFM (Recency, Frequency, Monetary) segmentation for all customers.
        Assigns customer segments: Champions, Loyal Customers, Potential Loyalists, At Risk, Lost.
        """
        sql_rfm_raw = """
        SELECT 
            c.customer_id,
            c.first_name || ' ' || c.last_name as customer_name,
            c.email,
            c.segment as customer_type,
            MAX(o.order_date) as last_order_date,
            COUNT(DISTINCT o.order_id) as frequency,
            COALESCE(SUM(o.total_amount), 0) as monetary
        FROM customers c
        JOIN orders o ON c.customer_id = o.customer_id
        WHERE o.status = 'Completed'
        GROUP BY c.customer_id, customer_name, c.email, c.segment;
        """
        
        with db.bind.connect() as conn:
            df = pd.read_sql_query(text(sql_rfm_raw), conn)

        if df.empty:
            return {"summary": [], "segment_counts": {}, "details": []}

        # Reference date for Recency (most recent order date in dataset + 1 day)
        df['last_order_date'] = pd.to_datetime(df['last_order_date'])
        max_date = df['last_order_date'].max() + pd.Timedelta(days=1)
        df['recency_days'] = (max_date - df['last_order_date']).dt.days

        # Compute RFM Scores (1 to 5 scale using quantiles)
        df['r_score'] = pd.qcut(df['recency_days'], q=5, labels=[5, 4, 3, 2, 1], duplicates='drop')
        df['f_score'] = pd.qcut(df['frequency'].rank(method='first'), q=5, labels=[1, 2, 3, 4, 5])
        df['m_score'] = pd.qcut(df['monetary'].rank(method='first'), q=5, labels=[1, 2, 3, 4, 5])

        df['r_score'] = df['r_score'].astype(int)
        df['f_score'] = df['f_score'].astype(int)
        df['m_score'] = df['m_score'].astype(int)

        # Segment Assignment Rule Engine
        def assign_segment(row):
            r, f, m = row['r_score'], row['f_score'], row['m_score']
            if r >= 4 and f >= 4 and m >= 4:
                return "Champions"
            elif f >= 3 and m >= 3:
                return "Loyal Customers"
            elif r >= 3 and f <= 2:
                return "Potential Loyalists"
            elif r <= 2 and f >= 3:
                return "At Risk"
            else:
                return "Lost / Needs Attention"

        df['rfm_segment'] = df.apply(assign_segment, axis=1)

        # Segment Aggregation
        segment_summary = df.groupby('rfm_segment').agg(
            customer_count=('customer_id', 'count'),
            avg_recency=('recency_days', 'mean'),
            avg_frequency=('frequency', 'mean'),
            total_monetary=('monetary', 'sum'),
            avg_monetary=('monetary', 'mean')
        ).reset_index()

        # Rounding metrics
        segment_summary['avg_recency'] = segment_summary['avg_recency'].round(1)
        segment_summary['avg_frequency'] = segment_summary['avg_frequency'].round(1)
        segment_summary['total_monetary'] = segment_summary['total_monetary'].round(2)
        segment_summary['avg_monetary'] = segment_summary['avg_monetary'].round(2)

        summary_list = segment_summary.to_dict(orient="records")
        top_customers = df.sort_values(by='monetary', ascending=False).head(20).to_dict(orient="records")

        # Format dates for JSON
        for c in top_customers:
            c['last_order_date'] = c['last_order_date'].strftime('%Y-%m-%d')

        return {
            "summary": summary_list,
            "top_customers": top_customers
        }
