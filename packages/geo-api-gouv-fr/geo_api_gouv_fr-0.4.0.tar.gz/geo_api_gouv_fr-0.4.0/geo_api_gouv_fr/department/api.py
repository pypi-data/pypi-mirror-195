import requests

from .schemas import (
    DepartmentsParams,
    DepartmentCodeParams,
    RegionDepartmentCodeParams
)


class Api:
    """
    Documentation : https://adresse.data.gouv.fr/api-doc/adresse
    """

    def __init__(self, **kwargs):
        self.url = kwargs.pop("url", "https://geo.api.gouv.fr")

    def departements(self, **kwargs) -> requests.Response:
        params = DepartmentsParams(**kwargs)
        return requests.get(self.url + "/departements", params=params.dict())

    def departements_by_code(self, **kwargs) -> requests.Response:
        params = DepartmentCodeParams(**kwargs)
        return requests.get(self.url + "/departements/" + params.code, params=params.dict())

    def departements_by_region(self, **kwargs) -> requests.Response:
        params = RegionDepartmentCodeParams(**kwargs)
        return requests.get(self.url + f"/regions/{params.regioncode}/departements", params=params.dict())
