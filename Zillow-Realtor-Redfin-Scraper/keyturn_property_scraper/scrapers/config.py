import random
from dataclasses import dataclass
from typing import Optional

from fake_useragent import UserAgent

from keyturn_property_scraper.scrapers.enums import ScraperName


def get_new_user_agent() -> str:
    return UserAgent(browsers=["edge", "chrome", "firefox", "safari", "opera"]).random


@dataclass
class ScraperLocationBounds:
    north: float
    west: float
    south: float
    east: float

    def to_map_bounds(self, scraper_name: ScraperName) -> dict:
        if scraper_name == ScraperName.ZILLOW:
            return {
                "west": self.west,
                "east": self.east,
                "south": self.south,
                "north": self.north,
            }
        elif scraper_name == ScraperName.REALTOR:
            return [
                [
                    [self.east, self.north],
                    [self.west, self.north],
                    [self.west, self.south],
                    [self.east, self.south],
                    [self.east, self.north],
                ]
            ]
        raise NotImplementedError(f"Scraper {scraper_name} is not implemented")


@dataclass
class BaseHeaders:
    accept_language: Optional[str] = "en-US,en;q=0.9"
    user_agent: Optional[str] = None
    accept: Optional[str] = "*/*"
    accept_encoding: Optional[str] = "gzip, deflate, br"
    _request_until_rotate_user_agent: Optional[int] = 0
    content_type: Optional[str] = "application/json"

    @property
    def rotated_user_agent(self):
        if self.user_agent is None:
            self.user_agent = get_new_user_agent()

        if self._request_until_rotate_user_agent >= 10:
            self.user_agent = get_new_user_agent()
            self._request_until_rotate_user_agent = 0
            return self.user_agent

        self._request_until_rotate_user_agent += 1
        return self.user_agent

    def get_base_headers(self, scraper_name: ScraperName) -> dict:
        if scraper_name == ScraperName.ZILLOW:
            return {
                "accept-language": self.accept_language,
                "user-agent": self.rotated_user_agent,
                "accept": self.accept,
                "accept-encoding": self.accept_encoding,
                "host": "www.zillow.com",
                "origin": "https://www.zillow.com",
                "cache-control": "no-cache",
                "connection": "keep-alive",
            }
        if scraper_name == ScraperName.REALTOR:
            return {
                "content-type": self.content_type,
                "host": "www.realtor.com",
                "origin": "https://www.realtor.com",
                "accept": "application/json",
                "accept-language": "en-US,en;q=0.9",
                "cache-control": "no-cache",
                "cache-control": "no-cache",
                "accept-encoding": "gzip, deflate, br",
                "user-agent": self.rotated_user_agent,
            }
        raise ValueError(f"Unknown scraper name: {scraper_name}")


@dataclass
class ScraperSleepTimeouts:
    list_request: int = .3
    detail_request: int = 1.2


@dataclass
class ScraperFilters:
    price_from: Optional[int] = None
    price_to: Optional[int] = None

    def get_filter_for_scraper(self, scraper_name: ScraperName) -> dict:
        if scraper_name == ScraperName.ZILLOW:
            return {
                "unformattedPrice": {
                    "min": self.price_from,
                    "max": self.price_to,
                }
            }
        else:
            raise ValueError(f"Unknown scraper name: {scraper_name}")


@dataclass
class ScraperConfig:
    market: any
    location_bounds: ScraperLocationBounds
    request_id: Optional[int] = 1
    base_headers: Optional[BaseHeaders] = BaseHeaders()
    timeouts: Optional[ScraperSleepTimeouts] = ScraperSleepTimeouts()
    additional_headers: Optional[any] = None
    filters: Optional[ScraperFilters] = ScraperFilters()
    use_redfin: Optional[bool] = True
    proxy: Optional[dict] = None

    @property
    def rotated_request_id(self) -> int:
        self.request_id += 1
        return self.request_id
