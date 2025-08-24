# app/features/images/models.py
# 画像を管理するためのORMモデル
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

# 親クラスPointの方でcascade="all, delete-orphan"を指定することで、親のPointが削除された時に関連する画像も削除されるようにする
class Image(Base):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    point_id = Column(Integer, ForeignKey("points.id"),nullable=False,index=True)
    bucket = Column(String, nullable=False)      # S3のバケット名
    object_key = Column(String, nullable=False)  # S3のオブジェクトキー
    photo_category = Column(String, nullable=False)  # 画像のカテゴリ（例：wholeTree,detail,base,leaves）
    point = relationship("Point", back_populates="image")