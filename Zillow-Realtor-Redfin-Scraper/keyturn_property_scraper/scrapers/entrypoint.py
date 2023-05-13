from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Type, Generator
    from keyturn_property_scraper.scrapers.base import BaseScraper
    from keyturn_property_scraper.scrapers.config import ScraperConfig
    from keyturn_property_scraper.scrapers.property import PropertyData


class ScraperEntrypoint:
    def __init__(self, scraper_class: "Type[BaseScraper]", config: "ScraperConfig"):
        self.scraper = scraper_class(config)

    def run(self) -> "Generator[PropertyData, None, None]":
        for p in self.scraper.properties:
            yield p
