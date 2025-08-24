## app/post/pin/schema.py
from pydantic import BaseModel, Field, AwareDatetime,ConfigDict
from typing import List,Optional
from fastapi import UploadFile

class PostPinRequest(BaseModel):

    model_config = ConfigDict(
    arbitrary_types_allowed=True,
    populate_by_name=True,
    )

    # common member
    category: str = Field(..., description="Category of the pin (Matsu or Nara)")
    lat: float = Field(..., description="reported pin's latitude (e.g. 35.000)")
    lng: float = Field(..., description="reported pin's longitude (e.g. 139.00)")
    start: str = Field(..., description="Start date in YYYY-MM-DD format (e.g., '2023-01-01')") #使わない
    end: str = Field(..., description="End date in YYYY-MM-DD format (e.g., '2023-12-31')") #使わない

    # optional member
    texture_rating: Optional[int] = Field(
        None,
        alias="textureRating",
        description="Matsu only. Provide ad integer rating (e.g. 1-5)",
    )
    hole_size: Optional[int] = Field(
        None,
        alias="holeSize",
        description="Nara only. Provide ad integer (e.g. 1-2)",
    )
    
    # images
    whole_tree: Optional[List[UploadFile]] = Field(
        None, 
        alias="wholeTree",
        description="One or more photos of the whole tree."
    )
    detail: Optional[List[UploadFile]] = Field(
        None, description="One or more photos of the whole tree."
    )
    base: Optional[List[UploadFile]] = Field(
        None, description="One or more photos of the whole tree."
    )
    leaves: Optional[List[UploadFile]] = Field(
        None, description="One or more photos of the whole tree."
    )

    
class PostPinResponse(BaseModel):
    status: str