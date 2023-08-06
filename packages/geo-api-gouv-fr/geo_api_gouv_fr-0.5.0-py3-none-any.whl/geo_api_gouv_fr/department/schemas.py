from pydantic import BaseModel
from typing import Optional, List


class DepartmentsParams(BaseModel):
    nom: Optional[str]
    codeRegion: Optional[str]
    code: Optional[str]
    limit: Optional[int]
    fields: Optional[List[str]]


class DepartmentCodeParams(BaseModel):
    code: Optional[str]
    fields: Optional[list]
    limit: Optional[int]


class RegionDepartmentCodeParams(BaseModel):
    regioncode: Optional[str]
    limit: Optional[int]


class DepartmentsResponse(BaseModel):

    nom: str
    code: int
    codeRegion: int
    fields: Optional[list]
    _score: Optional[float]
