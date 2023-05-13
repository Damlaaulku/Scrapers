import requests

from json import JSONDecodeError
from marshmallow import INCLUDE
from urllib.parse import urlencode

from keyturn_property_scraper.scrapers import BaseScraper, ScraperName
from keyturn_property_scraper.scrapers.schemas import ZillowPropertySchema
from keyturn_property_scraper.scrapers.exceptions import ScraperBoundsTooLargeException, ScraperBlockedException, \
    ScraperGracefulStopException


class ZillowScraper(BaseScraper):
    NAME = ScraperName.ZILLOW
    PROPERTY_SCHEMA_CLASS = ZillowPropertySchema

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._current_page = 1
        self.base_url = "https://www.zillow.com/search/GetSearchPageState.htm?"
        """
        Cat 1 is used for agent listings, and cat 2 for regular listings.
        When the methods _switch_categories called, the class starts receiving non-agent listings. 
        """
        self._category, self._total_category = "cat1", "cat2"
        self._category_totals = {
            "cat1": {
                "totalResultCount": 0
            },
            "cat2": {
                "totalResultCount": 0
            }
        }
        self._results_per_page = 0
        self._cookies = None

    def _switch_categories(self):
        self._category, self._total_category = "cat2", "cat1"

    def _increment_page(self):
        """
        The method paginates through properties by page, until all agent listings are received.
        After all listings received - the method switches to regular listings.
        When regular listings are received - the method stops
        :raise StopIteration: when all properties are received
        """
        def _has_next_page(current_page, total, per_page) -> bool:
            return current_page < (total // per_page) + 1

        if _has_next_page(self._current_page, self._category_totals[self._category]["totalResultCount"], self._results_per_page):
            self._current_page += 1
            return

        if self._category == "cat2":
            raise ScraperGracefulStopException()

        self._switch_categories()
        self._current_page = 1

    def _build_request_params(self):
        """
        Here for example we can use request build with configured headers and other staff
        """
        return {
            "searchQueryState": {
                "category": self._category,
                "pagination": {"currentPage": str(self._current_page)},
                "usersSearchTerm": self.config.market,
                "mapBounds": self.config.location_bounds.to_map_bounds(self.NAME),
                # "filters": self.config.filters.get_filter_for_scraper(self.NAME),
                "filterState": {
                    "sortSelection": {
                        "value": "pricea"
                    },
                    "isAllHomes": {
                        "value": True
                    },
                    "isManufactured": {
                        "value": False
                    },
                    "isLotLand": {
                        "value": False
                    }
                },
                "isListVisible": True,
                "mapZoom": 12,
            },
            "wants": {
                self._category: ["listResults"],
                self._total_category: ["total"],
                "regionResults": ["regionResults"],
            },
            "requestId": self.config.rotated_request_id,
        }

    def _get_properties(self):
        """
        Somehow get list of properties by page
        :return:
        """

        for i in range(0, 3):
            response = requests.get(
                self.base_url + urlencode(self._build_request_params()),
                headers=self.config.base_headers.get_base_headers(self.NAME),
                cookies=self._cookies,
                proxies=self.config.proxy,
            )

            try:
                self._cookies = response.cookies
                data = response.json()
            except (KeyError, JSONDecodeError):
                if i == 2:
                    self._cookies = None
                    raise ScraperBlockedException()
                continue

            self._category_totals = data["categoryTotals"]

            if self._category == "cat1" and self._category_totals[self._category]["totalResultCount"] > 500:
                raise ScraperBoundsTooLargeException()

            self._results_per_page = data[self._category]["searchList"]["resultsPerPage"]
            prev_category = self._category

            return data[prev_category]["searchResults"]["listResults"]

    @property
    def properties(self, **kwargs):

        while True:
            raw_properties = self._get_properties()

            parsed_properties = self.PROPERTY_SCHEMA_CLASS().load(raw_properties, many=True, unknown=INCLUDE)
            for p in parsed_properties:
                yield self.PROPERTY_SCHEMA_CLASS.to_property_data(p, use_redfin_data=self.config.use_redfin)

            self._increment_page()
            BaseScraper.configure_timeout(self) 
