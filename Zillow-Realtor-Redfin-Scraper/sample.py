from keyturn_property_scraper.scrapers import ZillowScraper, RealtorScraper, ScraperConfig, ScraperEntrypoint, ScraperLocationBounds
from keyturn_property_scraper.scrapers.exceptions import ScraperBlockedException, ScraperGracefulStopException

if __name__ == "__main__":
    instance = ScraperEntrypoint(
        RealtorScraper,
        ScraperConfig(
            market="Los Angeles",
            location_bounds=ScraperLocationBounds(
                **{"west": -157.77950332734682, "east": -157.7015690622101, "south": 21.35724892171078, "north": 21.419825827818954},
            ),
            use_redfin=False,
        )
    )
    total_found = 0


    def _get_props():
        global total_found

        try:
            for p in instance.run():
                print(f"Found: {p.id}")
                total_found += 1
        except ScraperBlockedException:
            _get_props()
        except ScraperGracefulStopException:
            print(f"Found {total_found} properties")


    _get_props()
