from unittest import TestCase
from .. import AdressApi, SearchResponse, ReverseResponse
import csv
import time
import requests
WAIT_TIME = 0.2


class TestAdress(TestCase):

    def setUp(self) -> None:
        self.api = AdressApi()
        return super().setUp()

    def test_search(self) -> requests.Response:
        time.sleep(WAIT_TIME)
        r = self.api.search(q="8+bd+du+port", limit=15)
        self.assertTrue(r.status_code == 200)
        r = self.api.search(q="8+bd+du+port", postcode=44380, limit=15)
        self.assertTrue(r.status_code == 200)
        r = self.api.search(q="8+bd+du+port", type="street", limit=15)
        self.assertTrue(r.status_code == 200)
        return r

    def test_search_csv(self) -> None:
        time.sleep(WAIT_TIME)
        r = self.api.search_csv(csv="./geo_api_gouv_fr/tests/data/search.csv", columns=["adresse", "postcode"])
        self.assertTrue(r.status_code == 200)
        with open("/app/testResults/searchcsv-simple.json", "wb") as f:
            f.write(r.content)
        r = self.api.search_csv(csv="./geo_api_gouv_fr/tests/data/search.csv",
                                postcode="postcode", columns=["adresse", "postcode"])
        self.assertTrue(r.status_code == 200)
        with open("/app/testResults/searchcsv-columns.json", "wb") as f:
            f.write(r.content)
        r = self.api.search_csv(csv="./geo_api_gouv_fr/tests/data/search.csv",
                                postcode="postcode", result_columns=["latitude", "longitude"])
        self.assertTrue(r.status_code == 200)
        with open("/app/testResults/searchcsv-postcode.json", "wb") as f:
            f.write(r.content)

    def test_reverse_csv(self) -> None:
        time.sleep(WAIT_TIME)
        r = self.api.reverse_csv(csv="./geo_api_gouv_fr/tests/data/reverse.csv")
        self.assertTrue(r.status_code == 200)
        with open("/app/testResults/reversecsv-simple.json", "wb") as f:
            f.write(r.content)

    def test_search_error(self) -> None:

        with self.assertRaises(ValueError):
            self.api.search(q="8+bd+du+port", type="noclue", limit=15)

    def test_reverse(self) -> requests.Response:
        time.sleep(WAIT_TIME)
        r = self.api.reverse(lon=2.37, lat=48.357)
        self.assertTrue(r.status_code == 200)
        return r

    def test_search_response(self) -> None:
        r = self.test_search()
        parsed = SearchResponse(**r.json())
        self.assertTrue(True)

    def test_reversed_response(self) -> None:
        r = self.test_reverse()
        parsed = ReverseResponse(**r.json())
        self.assertTrue(True)
