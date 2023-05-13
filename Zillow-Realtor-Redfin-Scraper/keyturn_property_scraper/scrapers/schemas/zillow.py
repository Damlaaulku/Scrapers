from marshmallow import Schema, fields, pre_load, INCLUDE

from keyturn_property_scraper.scrapers.schemas.base import BasePropertySchema
from keyturn_property_scraper.scrapers.property import PropertyData


class ZillowHomeInfoSchema(Schema):
    class Meta:
        unknown = INCLUDE

    city = fields.Str(missing=None, nullable=True, allow_none=True)
    zipcode = fields.Str(missing=None, nullable=True, allow_none=True)
    state = fields.Str(missing=None, nullable=True, allow_none=True)
    lotAreaValue = fields.Float(missing=None, nullable=True, allow_none=True)
    lotAreaUnit = fields.Str(missing=None, nullable=True, allow_none=True)
    zestimate = fields.Integer(missing=None, nullable=True, allow_none=True)
    homeType = fields.Str(missing=None, nullable=True, allow_none=True)


class ZillowHPDSchema(Schema):
    class Meta:
        unknown = INCLUDE

    homeInfo = fields.Nested(ZillowHomeInfoSchema())

    @pre_load
    def add_home_info_if_empty(self, data, **kwargs):
        if 'homeInfo' not in data:
            data['homeInfo'] = ZillowHomeInfoSchema().load({})
        return data


class ZillowLatLongSchema(Schema):
    class Meta:
        unknown = INCLUDE

    latitude = fields.Float(missing=None, nullable=True, allow_none=True)
    longitude = fields.Float(missing=None, nullable=True, allow_none=True)


class ZillowPropertySchema(BasePropertySchema, Schema):
    class Meta:
        unknown = INCLUDE

    id = fields.Str(required=True)
    addressStreet = fields.Str(missing=None, nullable=True, allow_none=True)
    unformattedPrice = fields.Integer(missing=None, nullable=True)
    imgSrc = fields.Str(missing=None, nullable=True, allow_none=True)
    baths = fields.Integer(missing=None, nullable=True, allow_none=True)
    beds = fields.Integer(missing=None, nullable=True, allow_none=True)
    area = fields.Integer(missing=None, nullable=True, allow_none=True)
    detailUrl = fields.Str(missing=None, nullable=True, allow_none=True)
    hdpData = fields.Nested(ZillowHPDSchema(many=False))
    latLong = fields.Nested(ZillowLatLongSchema(many=False))

    @pre_load
    def add_data_if_empty(self, data, **kwargs):
        if 'hdpData' not in data:
            data['hdpData'] = ZillowHPDSchema().load({})
        if 'latLong' not in data:
            data['latLong'] = ZillowLatLongSchema().load({})
        return data

    @classmethod
    def to_property_data(cls, data: dict, use_redfin_data: bool = True) -> PropertyData:
        description, year_built, hoa_dues, days_on_market = None, None, None, None
        return PropertyData(
            city=data["hdpData"]["homeInfo"]["city"],
            state=data["hdpData"]["homeInfo"]["state"],
            zip_code=data["hdpData"]["homeInfo"]["zipcode"],
            land_area=data['hdpData']['homeInfo']['lotAreaValue'] if data['hdpData']['homeInfo']['lotAreaValue'] else None,
            land_area_unit=data['hdpData']['homeInfo']['lotAreaUnit'] if data['hdpData']['homeInfo']['lotAreaUnit'] else None,
            property_estimate_value=data['hdpData']['homeInfo']['zestimate'] if data['hdpData']['homeInfo']['zestimate'] else None,
            latitude=data['latLong']['latitude'] if data['latLong']['latitude'] else None,
            longitude=data['latLong']['longitude'] if data['latLong']['longitude'] else None,
            id=data["id"],
            address=data["addressStreet"],
            price=data["unformattedPrice"],
            image=data["imgSrc"] if data["imgSrc"] else None,
            bathrooms=data["baths"] if data["baths"] else None,
            bedrooms=data["beds"] if data["beds"] else None,
            property_area=data["area"] if data["area"] else None,
            external_url=data["detailUrl"],
            home_type=data['hdpData']['homeInfo']["homeType"] if data['hdpData']['homeInfo']["homeType"] else None,
            description=description,
            year_built=year_built,
            hoa_dues=hoa_dues,
            days_on_market=days_on_market,
        )
