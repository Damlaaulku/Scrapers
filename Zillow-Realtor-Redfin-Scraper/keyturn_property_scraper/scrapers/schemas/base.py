from keyturn_property_scraper.scrapers.property import PropertyData


class BasePropertySchema:
    @classmethod
    def to_property_data(cls, data: dict) -> PropertyData:
        """Convert the schema to a property data object."""
        raise NotImplementedError()
