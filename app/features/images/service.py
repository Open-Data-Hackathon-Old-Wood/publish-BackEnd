## app/features/images/service.py
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.features.images.repository import ImageRepository
from app.features.images.schemas import ImageURLQuery, MatsuImageURLOut, NaraImageURLOut

class ImageService:
    def __init__(self, db: Session):
        self.repo = ImageRepository(db)

    # imageのURLを取得するメソッド. 画像のカテゴリごとにURLを取得し、ImageOutスキーマで返す.全てのカテゴリの画像が存在しない場合は404エラーを返す
    def get_matsu_image_urls(self, query: ImageURLQuery):
        try:
            wholeTree = self.repo.fetch_image_by_point_id(point_id=query.point_id, photo_category='wholeTree')
            leaves = self.repo.fetch_image_by_point_id(point_id=query.point_id, photo_category='leaves')
            detail = self.repo.fetch_image_by_point_id(point_id=query.point_id, photo_category='detail')
            base = self.repo.fetch_image_by_point_id(point_id=query.point_id, photo_category='base')
            # もし全てのカテゴリの画像が存在しない場合は404エラーを返す
            if ( wholeTree == "" and leaves == "" and detail == "" and base == ""):
                raise HTTPException(status_code=404, detail="Image not found for the given point ID and category")
            else:
                return MatsuImageURLOut(
                    wholeTree=wholeTree,
                    leaves=leaves,
                    detail=detail,
                    base=base,
                )
        except HTTPException as e:
            print(f"HTTPException: {e.detail}")
            return HTTPException(status_code=e.status_code, detail=e.detail)
        except Exception as e:
            print(f"Unexpected error: {e}")
            return HTTPException(status_code=500, detail="Internal server error")
        
    # imageのURLを取得するメソッド. 画像のカテゴリごとにURLを取得し、ImageOutスキーマで返す.全てのカテゴリの画像が存在しない場合は404エラーを返す
    def get_nara_image_urls(self, query: ImageURLQuery):
        try:
            wholeTree = self.repo.fetch_image_by_point_id(point_id=query.point_id, photo_category='wholeTree')
            detail = self.repo.fetch_image_by_point_id(point_id=query.point_id, photo_category='detail')
            base = self.repo.fetch_image_by_point_id(point_id=query.point_id, photo_category='base')
            # もし全てのカテゴリの画像が存在しない場合は404エラーを返す
            if ( wholeTree == "" and detail == "" and base == ""):
                raise HTTPException(status_code=404, detail="Image not found for the given point ID and category")
            else:
                return NaraImageURLOut(
                    wholeTree=wholeTree,
                    detail=detail,
                    base=base,
                )
        except HTTPException as e:
            print(f"HTTPException: {e.detail}")
            return HTTPException(status_code=e.status_code, detail=e.detail)
        except Exception as e:
            print(f"Unexpected error: {e}")
            return HTTPException(status_code=500, detail="Internal server error")