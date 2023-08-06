import requests

from .schemas import (
    RegionsParams,
    RegionCodeParams
)


class Api:
    """
    Documentation : https://adresse.data.gouv.fr/api-doc/adresse
    """

    def __init__(self, **kwargs):
        self.url = kwargs.pop("url", "https://geo.api.gouv.fr")

    def regions(self, **kwargs) -> requests.Response:
        params = RegionsParams(**kwargs)
        return requests.get(self.url + "/regions", params=params.dict())

    def regions_by_code(self, **kwargs) -> requests.Response:
        params = RegionCodeParams(**kwargs)
        return requests.get(self.url + "/regions/" + params.code, params=params.dict())
