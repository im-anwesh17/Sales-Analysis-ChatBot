from app.db.session import engine, Base
from app.db import models  # Ensure all models are imported
from app.core.logging import logger


def init_db():
    logger.info("Initializing database tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables initialized successfully.")


if __name__ == "__main__":
    init_db()
