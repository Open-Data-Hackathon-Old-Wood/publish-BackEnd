## app/features/pin_detail/nara/router.py
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.features.pin_detail.nara.schemas import NaraDetailQuery,NaraDetailResponse
from app.features.pin_detail.nara.service import NaraDetailService

router = APIRouter(prefix="/pins/nara", tags=["pins"])

# マツ枯れの詳細情報を取得するエンドポイント
@router.get("/detail",response_model=NaraDetailResponse)
def get_pin_detail_nara(
    category: str = Query(..., description="Category of the wood (matsu or nara)"),
    lng: float = Query(..., description="current longitude (WGS84)"),
    lat: float = Query(..., description="current latitude (WGS84)"),
    start: str = Query(..., description="Start date in YYYY-MM-DD format"),
    end: str = Query(..., description="End date in YYYY-MM-DD format"),
    db: Session = Depends(get_db),
):
    query = NaraDetailQuery(category=category,lng=lng, lat=lat,start=start,end=end)
    svc = NaraDetailService(db)
    return svc.get_pin_detail_nara(query=query)