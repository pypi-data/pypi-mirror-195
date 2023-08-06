import requests
import os
from .schemas import (
    SearchParams,
    SearchCSVParams,
    ReverseParams
)


class Api:
    """
    Documentation : https://adresse.data.gouv.fr/api-doc/adresse
    """

    def __init__(self, **kwargs):
        self.url = kwargs.get("url", "https://api-adresse.data.gouv.fr")

    def search(self, **kwargs) -> requests.Response:
        params = SearchParams(**kwargs)
        return requests.get(self.url + "/search", params=params.dict())

    def reverse(self, **kwargs) -> requests.Response:
        params = ReverseParams(**kwargs)
        return requests.get(self.url + "/reverse", params=params.dict())

    def search_csv(self, csv: str, **kwargs) -> requests.Response:

        # read the csv file
        if not os.path.isfile(csv):
            raise FileNotFoundError(csv)

        # check max size
        file_stats = os.stat(csv)
        file_size = file_stats.st_size / (1024 * 1024)
        if file_size > 50:
            print(f"csv file size is too big (>50Mo), current size : {file_size}")
            return None

        params = SearchCSVParams(**kwargs)

        with open(csv, 'r') as f:
            r = requests.post(self.url + "/search/csv/", data=params.dict(), files={'data': f})

        return r

    def reverse_csv(self, csv: str) -> requests.Response:

        # read the csv file
        if not os.path.isfile(csv):
            raise FileNotFoundError(csv)

        # check max size
        file_stats = os.stat(csv)
        file_size = file_stats.st_size / (1024 * 1024)
        if file_size > 6:
            print(f"csv file size is too big (>50Mo), current size : {file_size}")
            return None

        with open(csv, 'r') as f:
            r = requests.post(self.url + "/search/csv/", files={'data': f})

        return r
