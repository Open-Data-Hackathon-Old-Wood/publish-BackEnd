from pydantic import BaseModel

class BBox(BaseModel):
    west: float
    south: float
    east: float
    north: float