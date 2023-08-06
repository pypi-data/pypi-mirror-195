from pydantic import BaseModel
from typing import Optional


class RegionsParams(BaseModel):
    nom: Optional[str]
    code: Optional[str]
    limit: Optional[int]


class RegionCodeParams(BaseModel):
    code: Optional[str]
    code: Optional[str]
    limit: Optional[int]


class RegionsResponse(BaseModel):

    nom: str
    code: int
    _score: Optional[float]
