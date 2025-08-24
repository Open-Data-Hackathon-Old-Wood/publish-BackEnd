# /app/post/pin/mats/router
from fastapi import APIRouter, Depends, HTTPException, status, Form, File, UploadFile
from sqlalchemy.orm import Session
from typing import Optional,List
from app.core.deps import get_db
from app.core.config import settings
from app.infrastructure.storage.minio import MinioStorage
from app.post.pin.nara.schemas import PostPinRequest, PostPinResponse
from app.post.pin.nara.service import PinWriteService
from app.post.pin.nara.repository import RepositoryError

# ナラ枯れのデータを登録する用のAPI
router = APIRouter(prefix="/register/nara",tags=["pins:nara:write"],)
def _parse_post_form(
    category: str = Form(...),
    lat: float = Form(...),
    lng: float = Form(...),
    start: str = Form(...),
    end: str = Form(...),
    textureRating: Optional[int] = Form(None),
    holeSize: Optional[int] = Form(None),
    wholeTree: Optional[List[UploadFile]] = File(None),
    detail: Optional[List[UploadFile]] = File(None),
    base: Optional[List[UploadFile]] = File(None),
    leaves: Optional[List[UploadFile]] = File(None),
) -> PostPinRequest:
    return PostPinRequest(
        category=category,
        lat=lat,
        lng=lng,
        start=start,
        end=end,
        textureRating=textureRating,
        holeSize=holeSize,
        wholeTree=wholeTree,
        detail=detail,
        base=base,
        leaves=leaves,
    )

def get_storage() -> MinioStorage:
    return MinioStorage()

@router.post("",response_model=PostPinResponse,status_code=status.HTTP_201_CREATED,summary="Create a new Matsu pin (with optional images)",)
def create_nara_pin(
    req: PostPinRequest = Depends(_parse_post_form),
    db: Session = Depends(get_db),
    storage: MinioStorage = Depends(get_storage),):
    service = PinWriteService(db, storage)
    try:
        service.create_pin_with_images(req)
    except RepositoryError as e:
        raise HTTPException(status_code=500, detail=str(e))

    return PostPinResponse(
        status="true",
    )