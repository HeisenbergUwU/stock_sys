from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from core.constaint import *
import os

load_dotenv()

__all__ = ["session"]

db_user = os.getenv("DB_USER", "root")
db_password = os.getenv("DB_PASSWORD", "123456")
db_host = os.getenv("DB_HOST", "localhost")
db_port = os.getenv("DB_PORT", 3306)
db_database = os.getenv("DB_DATABASE", "stock")


DATABASE_URL = (
    f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_database}"
)


engine = create_engine(DATABASE_URL, echo=USE_SQL)

session = sessionmaker(bind=engine, autocommit=False, autoflush=False)
