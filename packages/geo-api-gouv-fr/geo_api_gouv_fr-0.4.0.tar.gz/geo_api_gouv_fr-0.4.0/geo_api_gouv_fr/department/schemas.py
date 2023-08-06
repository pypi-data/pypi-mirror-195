from pydantic import BaseModel
from typing import Optional


class DepartmentsParams(BaseModel):
    nom: Optional[str]
    limit: Optional[int]


class DepartmentCodeParams(BaseModel):
    code: Optional[str]
    limit: Optional[int]


class RegionDepartmentCodeParams(BaseModel):
    regioncode: Optional[str]
    limit: Optional[int]


class DepartmentsResponse(BaseModel):

    nom: str
    code: int
    codeRegion: int
    _score: Optional[float]
