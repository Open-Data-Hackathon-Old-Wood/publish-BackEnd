## app/core/deps.py
from typing import Generator
from sqlalchemy.orm import Session
from app.db.session import SessionLocal

# DBセッションを取得し、接続・終了処理を行う
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()