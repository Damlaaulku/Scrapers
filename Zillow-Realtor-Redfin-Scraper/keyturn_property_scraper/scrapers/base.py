import abc
from typing import Generator
import random
import time

from keyturn_property_scraper.scrapers.config import ScraperConfig
from keyturn_property_scraper.scrapers.enums import ScraperName
from keyturn_property_scraper.scrapers.property import PropertyData


class BaseScraper(abc.ABC):
    NAME: ScraperName = None

    def __init__(self, config: ScraperConfig):
        """Initialize the scraper."""
        self.config = config

    def update_config(self, config: ScraperConfig):
        self.config = config

    def configure_timeout(self):
        initial_timeout_ms = self.config.timeouts.list_request * 1000
        random_sleep = abs(random.randint(initial_timeout_ms - 500, initial_timeout_ms + 500))
        time.sleep(random_sleep / 1000)

    @property
    @abc.abstractmethod
    def properties(self) -> Generator[PropertyData, None, None]:
        """Get the properties from the scraper."""
