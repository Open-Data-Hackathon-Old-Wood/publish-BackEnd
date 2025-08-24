## app/features/pin_detail/nara/service.py
from zoneinfo import ZoneInfo
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.features.pin_detail.nara.repository import NaraDetailRepository
from app.features.pin_detail.nara.schemas import NaraDetailQuery, NaraDetailResponse,NaraDetailOut,PhotoUrls
from app.features.pin_detail.nara.models import PointDetailNara as Nara
from app.features.images.schemas import ImageURLQuery, NaraImageURLOut, NaraImageURLOut
from app.features.images.service import ImageService

class NaraDetailService:
    def __init__(self, db: Session):
        self.repo = NaraDetailRepository(db)

    # naraのピンの詳細情報を取得するメソッド. 普通はPinがあればPinDetailもあるはずだけど、万が一Nullが返ってきた場合はstatus code 404を返す
    def get_pin_detail_nara(self, query: NaraDetailQuery):
        try:
            point = self.repo.fetch_point_id(category=query.category, lng=query.lng, lat=query.lat, start=query.start, end=query.end)
            if point is None:
                raise ValueError("No pin found at the specified location.")
            detail_info = self.repo.fetch_point_detail(point_id=point["id"])
            if detail_info is None:
                raise ValueError("No detail found for the specified pin.")
            
            matsu_image_service = ImageService(self.repo.db)
            image_query = ImageURLQuery(point_id=point["id"], photo_category="")
            image_urls = matsu_image_service.get_nara_image_urls(image_query)

            return NaraDetailResponse(
                id=str(point["id"]),
                category=query.category,
                lat=query.lat,
                lng=query.lng,
                start=query.start,
                end=query.end,
                texture_rating=None,
                hole_size=detail_info["needle_size"],
                photo_urls=PhotoUrls(
                    whole_tree=[image_urls.wholeTree],
                    detail=[image_urls.detail],
                    base=[image_urls.base],
                ),
                created_at=point["created_at"],
            )
            
        except ValueError as e:
            print(f"Error fetching pin details: {e}")
            return HTTPException(status_code=404, detail="Pin not found")
        except Exception as e:
            print(f"Unexpected error: {e}")