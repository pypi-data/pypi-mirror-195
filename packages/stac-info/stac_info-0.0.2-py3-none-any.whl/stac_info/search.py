from typing import TextIO
from urllib.parse import urlencode
import logging
import requests
import csv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EarthSearch:
    """
    Represents the Earth Search API
    """

    def __init__(self, url):
        self.url = url

    def get_number_of_matches(self, bbox, date) -> int:
        """
        :param bbox: bounding box coordinates
        :type bbox: list
        :param date: date range to search
        :type date: str
        :return: a dictionary of the cloud cover query
        :rtype: dict
        """

        if bbox is None:
            bbox = []
        assert isinstance(bbox, list), "Bounding Box needs to be a list"
        assert isinstance(date, str), "Date argument should be string"

        try:
            query = urlencode({
                "bbox": bbox,
                "limit": 1,
                "datetime": date
            })
            response = requests.get(f"{self.url}?{query}")
            data = response.json()
        except Exception as e:
            logger.error(f"[ERROR]  {str(e)}")
            data = {"error": str(e)}
        return int(data["context"]["matched"])

    def filter(self, bbox: list, date: str, limit=10) -> TextIO:
        """
        :param bbox: bounding box coordinates
        :type bbox: list
        :param date: date range to search
        :type date: str
        :param limit: number of results to return
        :type limit: int
        :return: a list of the features that match the query
        :rtype: list
        """
        data_features = []

        assert isinstance(date, str), "Date argument should be string"
        assert isinstance(date, str), "Date argument should be string"
        number_of_matches = self.get_number_of_matches(bbox=bbox, date=date)
        number_of_pages = number_of_matches // limit
        last_page_number = number_of_matches % limit
        if last_page_number > 0:
            number_of_pages += 1
            for page in range(1, number_of_pages + 1):
                logger.info(f"Loading page {page} of {number_of_pages}")
                query = urlencode({
                    "bbox": bbox,
                    "datetime": date,
                    "limit": limit,
                    "page": page
                })
                try:
                    response = requests.get(f"{self.url}?{query}")
                    data = response.json()
                    data_features.extend(data["features"])
                except Exception as e:
                    logger.error(f"{str(e)}")
        with open("earth_search.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["id", "date", "cloud_cover", "geometry"])
            for feature in data_features:
                writer.writerow([
                    feature["id"],
                    feature["properties"]["datetime"],
                    feature["properties"]["eo:cloud_cover"],
                    feature["geometry"],
                ])
        logger.info(f"Total number of matches: {number_of_matches}")
        logger.info(f"Final search results written to earth_search.csv")
