# app/features/pins_detail/nara/models.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

# ナラ枯れのピンの詳細情報を管理するためのORMモデル。ナラの場合のみ、needle_sizeを持つ
class PointDetailNara(Base):
    __tablename__ = "point_details_nara"
    point_id = Column(Integer, ForeignKey("points.id"), primary_key=True)
    needle_size = Column(Integer, nullable=False)
    notes = Column(String)
    point = relationship("Point", back_populates="detail_nara")