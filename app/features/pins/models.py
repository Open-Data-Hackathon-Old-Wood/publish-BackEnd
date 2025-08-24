## app/features/pins/models.py
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy import Column,Integer,String,DateTime,ForeignKey,func
from geoalchemy2 import Geometry
from app.db.base import Base
from app.features.pin_detail.nara.models import PointDetailNara
from app.features.pin_detail.matsu.models import PointDetailMatsu
from app.features.images.models import Image

# DB上のpointsテーブルを定義するためのORMモデル.pointsはピンのidと座標、木のカテゴリーの情報を持つ
# cascade="all, delete-orphan"を指定して、親のPointが削除された時に関連する詳細情報や画像も削除されるようにする
class Point(Base):
    __tablename__ = "points"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    category = Column(String(8))
    geom = Column(Geometry(geometry_type="POINT", srid=4326), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now(), nullable=False)
    detail_nara = relationship("PointDetailNara", back_populates="point", uselist=False,cascade="all, delete-orphan")
    detail_matsu = relationship("PointDetailMatsu", back_populates="point", uselist=False,cascade="all, delete-orphan")
    image = relationship("Image", back_populates="point", cascade="all, delete-orphan")