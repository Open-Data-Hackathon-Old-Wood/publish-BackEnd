# app/features/pins_detail/matsu/models.py
# 松のピンの詳細情報を管理するためのORMモデル。（DBのテーブルと完全に対応）.マツガレのみ、helth_statusを持つ
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

# サーバー側で、各値を受け取った時のデフォルト値を定義しておく
class PointDetailMatsu(Base):
    __tablename__ = "point_details_matsu"

    point_id = Column(Integer, ForeignKey("points.id"), primary_key=True, index=True, nullable=False)
    health_status = Column(Integer, nullable=False)
    notes = Column(String, nullable=False)
    point = relationship("Point", back_populates="detail_matsu")