import requests

from json import JSONDecodeError
from marshmallow import INCLUDE

from keyturn_property_scraper.scrapers import BaseScraper, ScraperName
from keyturn_property_scraper.scrapers.schemas import RealtorPropertySchema
from keyturn_property_scraper.scrapers.exceptions import ScraperBlockedException, ScraperGracefulStopException


class RealtorScraper(BaseScraper):
    NAME = ScraperName.REALTOR
    PROPERTY_SCHEMA_CLASS = RealtorPropertySchema

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._current_page = 1
        self._limit = 20
        self._total = 0
        self.base_url = "https://www.realtor.com/api/v1/hulk?client_id=rdc-x&schema=vesta"

    def _increment_page(self):
        """
        The method paginates through properties by page, until all agent listings are received.
        After all listings received - the method switches to regular listings.
        When regular listings are received - the method stops
        :raise StopIteration: when all properties are received
        """
        def _has_next_page(current_page, total, per_page) -> bool:
            return current_page < (total // per_page) + 1

        if _has_next_page(self._current_page, self._total, self._limit):
            self._current_page += 1
            return

        raise ScraperGracefulStopException()

    def _build_request_params(self):
        """
        Here for example we can use request build with configured headers and other staff
        """
        return {
            "query": "\nquery ConsumerSearchQuery($query: HomeSearchCriteria!, $limit: Int, $offset: Int, $sort: [SearchAPISort], $sort_type: SearchSortType, $client_data: JSON, $bucket: SearchAPIBucket)\n{\n  home_search: home_search(query: $query,\n    sort: $sort,\n    limit: $limit,\n    offset: $offset,\n    sort_type: $sort_type,\n    client_data: $client_data,\n    bucket: $bucket,\n  ){\n    count\n    total\n    results {\n      property_id\n      list_price\n      primary_photo (https: true){\n        href\n      }\n      listing_id\n      virtual_tours{\n        href\n        type\n      }\n      status\n      permalink\n      price_reduced_amount\n      description{\n        beds\n        baths\n        baths_full\n        baths_3qtr\n        baths_half\n        sqft\n        lot_sqft\n        baths_max\n        baths_min\n        beds_max\n        sqft_min\n        sqft_max\n        type\n        sold_price\n        sold_date\n      }\n      location{\n        street_view_url\n        address{\n          line\n          postal_code\n          state\n          state_code\n          city\n          coordinate {\n            lat\n            lon\n          }\n        }\n      }\n      open_houses {\n        start_date\n        end_date\n      }\n      flags{\n        is_coming_soon\n        is_new_listing (days: 14)\n        is_price_reduced (days: 30)\n        is_foreclosure\n        is_new_construction\n        is_pending\n        is_contingent\n      }\n      list_date\n      photos(limit: 1, https: true){\n        href\n      }\n    }\n  }\n}",
            "variables": {
                "query": {
                    "status": [
                        "for_sale"
                    ],
                    "primary": True,
                    "boundary": {
                        "type": "Polygon",
                        "coordinates": self.config.location_bounds.to_map_bounds(self.NAME),
                    }
                },
                "limit": self._limit,
                "offset": (self._current_page - 1) * self._limit,
                "zohoQuery": {
                    "silo": "search_result_page",
                    "location": self.config.market,
                    "property_status": "for_sale",
                    "filters": {},
                    "page_index": str(self._current_page)
                },
                "sort_type": "relevant",
                "by_prop_type": [
                    "home"
                ]
            },
            "callfrom": "SRP",
            "nrQueryType": "MAP_MAIN_SRP",
            "isClient": True
        }

    def _get_properties(self):
        """
        Somehow get list of properties by page
        :return:
        """

        for i in range(0, 3):
            response = requests.post(url=self.base_url, json=self._build_request_params(), headers=self.config.base_headers.get_base_headers(self.NAME))
            try:
                data = response.json()
                self._total = data["data"]["home_search"]["total"]
                return data["data"]["home_search"]["results"]
            except (KeyError, JSONDecodeError):
                if i == 2:
                    raise ScraperBlockedException()
                continue

    @property
    def properties(self, **kwargs):

        while True:
            raw_properties = self._get_properties()

            parsed_properties = self.PROPERTY_SCHEMA_CLASS().load(raw_properties, many=True, unknown=INCLUDE)
            for p in parsed_properties:
                yield self.PROPERTY_SCHEMA_CLASS.to_property_data(p)

            self._increment_page()

            BaseScraper.configure_timeout(self)
