# 📊 AI Sales Analytics Chatbot

A production-quality, full-stack AI-powered Sales Analytics Chatbot built with **FastAPI**, **PostgreSQL**, **SQLAlchemy**, **Pandas**, **React**, **Tailwind CSS**, and **Recharts**.

Users can view executive dashboards, perform RFM Customer Segmentation, and ask natural language business questions. The AI engine converts natural language to optimized SQL queries, executes them safely against PostgreSQL, renders dynamic Recharts visualizations (Bar, Line, Pie, Metric), and synthesizes executive business summaries.

![Sales Analytics Banner](https://img.shields.io/badge/Python-3.12-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-emerald.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue.svg)
![React](https://img.shields.io/badge/React-18-cyan.svg)
![Tailwind CSS](https://img.shields.io/badge/Tailwind-3.4-sky.svg)

---

## 🌟 Key Features

1. **Executive Sales Dashboard**
   - Live KPI Metrics (Total Revenue, Completed Orders, Average Order Value, Active Customers, Monthly Growth).
   - Time-series monthly revenue trends (Recharts Area/Line Chart).
   - Revenue breakdown by category and regional state maps.
   - Ranked top 10 products table with unit volume and margin contribution.

2. **Natural Language to SQL (Text-to-SQL)**
   - Converts questions like *"What were the top 5 selling products by revenue?"* or *"Show monthly sales trends"* into optimized SQL.
   - Built-in SQL Sanitizer with AST/Regex validation: permits read-only `SELECT`/`WITH` statements and blocks `DROP`, `DELETE`, `UPDATE`, `INSERT`, `ALTER`, or multi-statement injections.

3. **AI Executive Insights**
   - For every executed query, the AI service synthesizes a 2-3 sentence executive summary explaining key takeaways, growth rates, or category leaders.

4. **Dynamic Recharts Renderer**
   - Automatically determines whether to display a Line Chart (time-series), Pie Chart (category share), Bar Chart (rankings), or Metric Card based on the returned dataset structure.

5. **Customer RFM Segmentation Engine**
   - Computes Recency, Frequency, and Monetary scores using Pandas quantile binning (`pd.qcut`).
   - Categorizes customers into 5 strategic segments: `Champions`, `Loyal Customers`, `Potential Loyalists`, `At Risk`, and `Lost`.

---

## 🛠️ Tech Stack

- **Backend**: Python 3.12, FastAPI, SQLAlchemy 2.0, PostgreSQL, Pandas, Pydantic v2
- **Frontend**: React 18, Vite, Tailwind CSS, Recharts, Lucide Icons, Axios
- **AI Integration**: Google Gemini API / OpenAI API SDKs + Built-in Rule Engine Fallback
- **DevOps**: Docker, Docker Compose, Pytest, Uvicorn

---

## 📁 Repository Structure

```
Sales Analysis Chatbot/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── router.py
│   │   │   └── v1/ (health.py, dashboard.py, analytics.py, chat.py)
│   │   ├── core/ (config.py, logging.py)
│   │   ├── db/ (session.py, models.py, init_db.py)
│   │   ├── schemas/ (chat.py, dashboard.py)
│   │   └── services/ (ai_service.py, sql_executor.py, analytics_service.py)
│   ├── main.py
│   ├── seed.py (Data Seeder Script)
│   ├── test_backend.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/ (Navbar, Dashboard, Chat, Analytics)
│   │   ├── services/ (api.js)
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── package.json
│   ├── vite.config.js
│   └── Dockerfile
├── docs/
│   ├── architecture.md
│   ├── db_schema.md
│   └── interview_prep.md
├── docker-compose.yml
└── README.md
```

---

## 🚀 Quickstart Guide

### Option 1: Run with Docker Compose (Recommended)

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/sales-analytics-chatbot.git
   cd sales-analytics-chatbot
   ```

2. Launch full application stack:
   ```bash
   docker-compose up --build
   ```

3. Open your browser:
   - **Frontend UI**: `http://localhost:5173`
   - **FastAPI API Docs**: `http://localhost:8000/docs`

---

### Option 2: Local Development Setup

#### 1. Backend Setup
```bash
cd backend
py -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Unix/macOS:
source .venv/bin/activate

pip install -r requirements.txt
python seed.py
uvicorn app.main:app --reload --port 8000
```

#### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

---

## 📚 Documentation & Interview Guide

- **[System Architecture](docs/architecture.md)**: Detailed breakdown of the Text-to-SQL pipeline, SQL sanitizer, and dynamic chart engine.
- **[Database Schema & Data Dictionary](docs/db_schema.md)**: ER diagrams, index definitions, and column definitions.
- **[Interview Preparation Guide](docs/interview_prep.md)**: Comprehensive answers to 20+ expected Senior Python, Data Analytics, and AI Engineer interview questions.

---

## 🧪 Running Automated Tests

```bash
cd backend
python test_backend.py
```
