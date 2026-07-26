# Architecture Explanation & System Design

The **AI Sales Analytics Chatbot** is designed with a high-performance, decoupled architecture separating the API Gateway, AI Translation Layer, Analytics Engine, and Interactive Frontend.

## High-Level Data & Request Lifecycle

```
[ User Input (Natural Language) ]
                │
                ▼
      [ React Chat Interface ]
                │ (HTTP POST /api/v1/chat/query)
                ▼
       [ FastAPI API Router ]
                │
                ▼
       [ AI Service Engine ]
                │ ──► Inject Database Schema & Rules Prompt
                │ ──► Call LLM (Gemini / OpenAI API / Heuristic Engine)
                │ ──► Extract Clean SQL
                ▼
     [ SQL Validator & Sanitizer ]
                │ ──► Check SELECT-only constraint
                │ ──► Regex search for forbidden DDL/DML keywords (DROP, DELETE, UPDATE)
                │ ──► Multi-statement execution blocking (semicolon check)
                ▼
     [ Database Execution Layer ]
                │ ──► Execute safe query against PostgreSQL / SQLAlchemy
                │ ──► Stream tabular output into Pandas DataFrame
                ▼
       [ Multi-Output Synthesizer ]
                ├──► [ Dynamic Chart Engine ] ──► Computes X/Y axis & Recharts type (Bar/Line/Pie)
                ├──► [ AI Business Summarizer ] ──► Synthesizes 2-3 sentence executive commentary
                └──► [ Formatter ] ──► Formats JSON response payload
                │
                ▼
      [ React Visual Response ]
```

---

## Technical Component Deep-Dive

### 1. Natural Language to SQL Engine (`ai_service.py`)
- **Schema Prompting**: Injects schema definitions (tables, column types, FK relationships, valid categorical strings) into the system context.
- **SQL Parsing & Cleanup**: Automatically strips markdown blocks (` ```sql ... ``` `) and trailing semicolons.
- **Heuristic Fallback Engine**: If no API keys are provided or network errors occur, a fallback rule-based engine evaluates intent keywords (`top products`, `monthly trend`, `regional`, `category`) to return valid parameterized SQL.

### 2. SQL Validator & Sanitizer (`sql_executor.py`)
- **Read-Only Enforcer**: Guarantees queries begin with `SELECT` or `WITH` (Common Table Expressions).
- **Forbidden Keyword Filter**: Scans AST/tokens for mutation commands (`DROP`, `DELETE`, `UPDATE`, `INSERT`, `ALTER`, `TRUNCATE`, `EXEC`).
- **Multi-Statement Guard**: Prevents SQL injection chaining by enforcing a single statement policy.
- **Safety Limit Injection**: Automatically appends `LIMIT 100` if the generated query omits explicit pagination bounds.

### 3. RFM Customer Analytics Engine (`analytics_service.py`)
- **Recency**: Calculates `days_since_last_order` relative to dataset max order timestamp.
- **Frequency**: Counts distinct completed orders per customer (`COUNT(DISTINCT order_id)`).
- **Monetary**: Sums gross completed spend (`SUM(total_amount)`).
- **Quantile Binning**: Assigns 1-5 relative scores using Pandas `pd.qcut` and ranks.
- **Segment Mapping Matrix**:
  - `Champions`: R >= 4, F >= 4, M >= 4
  - `Loyal Customers`: F >= 3, M >= 3
  - `Potential Loyalists`: R >= 3, F <= 2
  - `At Risk`: R <= 2, F >= 3
  - `Lost / Needs Attention`: R <= 2, F <= 2

### 4. Dynamic Chart Recommender (`recommend_chart_type`)
Evaluates the structure of the returned SQL DataFrame:
- If date/time columns exist (`month`, `order_date`, `year`) -> Recommends **Line / Area Chart**.
- If row count <= 5 and categorical breakdown exists (`category`, `segment`, `status`) -> Recommends **Pie / Donut Chart**.
- If general key-value or ranked listing -> Recommends **Bar Chart**.
- If 1 row & 1 column -> Recommends **Metric Card**.
