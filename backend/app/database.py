# 数据库连接与会话管理（MySQL）
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from backend.app.core.config import settings

# 根据 DATABASE_URL 创建引擎
engine = create_engine(
    settings.database_url,
    # 每次拿连接前先检查是否还活着，避免 MySQL 超时断连后报错
    pool_pre_ping=True,
)

# 会话工厂
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()