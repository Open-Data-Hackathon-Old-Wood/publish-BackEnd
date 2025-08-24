## app/features/pin_detail/matsu/router.py
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.features.pin_detail.matsu.schemas import MatsuDetailQuery,MatsuDetailResponse
from app.features.pin_detail.matsu.service import MatsuDetailService

router = APIRouter(prefix="/pins/matsu", tags=["pins"])

# マツ枯れの詳細情報を取得するエンドポイント.木の種類と位置情報、期間を指定して、マツ枯れの詳細情報を取得する
@router.get("/detail",response_model=MatsuDetailResponse)
def get_pin_detail_matsu(
    category: str = Query(..., description="Category of the wood (matsu or nara)"),
    lat: float = Query(..., description="current latitude (WGS84)"),
    lng: float = Query(..., description="current longitude (WGS84)"),
    start: str = Query(..., description="Start date in YYYY-MM-DD format"),
    end: str = Query(..., description="End date in YYYY-MM-DD format"),
    db: Session = Depends(get_db),
):
    # フロント側ですでに期間はフィルタリングされていたはずなので、ここではlonとlatだけを使ってピンの詳細情報を取得する
    query = MatsuDetailQuery(category=category,lat=lat,lng=lng,start=start,end=end)
    svc = MatsuDetailService(db)
    return svc.get_pin_detail_matsu(query=query)