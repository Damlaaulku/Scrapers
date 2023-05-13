# Keyturn Property scraper

## publishing package

1. Add custom PyPi repository
    ```bash
    poetry config repositories.packagr https://api.packagr.app/nQQS8Bs9
    ```
    and set up credentials
    ```bash
    poetry config http-basic.packagr email@keyturn.homes
    ```
2. Update version of the package in `pyproject.toml`
3. Publish package
    ```bash
    poetry publish --build -r packagr
    ```
   
## Installing package

1. Modify pyproject.toml and add custom PyPi repository
    ```toml
    [[tool.poetry.source]]
    name = "packagr"
    url = "https://api.packagr.app/nQQS8Bs9/"
    secondary = true
    ```
2. Install package
    ```bash
    poetry add keyturn-property-scraper --source packagr
    ```

### Example of usage

```python
from keyturn_property_scraper.scrapers import ZillowScraper, ScraperConfig, ScraperLocationBounds, BaseHeaders, ScraperEntrypoint

instance = ScraperEntrypoint(
    ZillowScraper,
    ScraperConfig(
        market="Los Angeles",
        location_bounds=ScraperLocationBounds(
            north=37.8199,
            west=-122.4783,
            south=37.7034,
            east=-122.3482,
        ),
        base_headers=BaseHeaders(
            accept_language="en-US,en;q=0.9",
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
            accept="text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            accept_encoding="gzip, deflate, br"
        ),
        request_id=4
    )
)

instance.run()
```
