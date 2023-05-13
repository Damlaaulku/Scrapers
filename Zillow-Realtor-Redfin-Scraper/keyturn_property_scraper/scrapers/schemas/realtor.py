from marshmallow import Schema, fields, pre_load, INCLUDE

from keyturn_property_scraper.scrapers.schemas.base import BasePropertySchema
from keyturn_property_scraper.scrapers.property import PropertyData


class RealtorCoordinateSchema(Schema):
    class Meta:
        unknown = INCLUDE

    lat = fields.Float(missing=None, nullable=True, allow_none=True)
    lon = fields.Float(missing=None, nullable=True, allow_none=True)


class RealtorAddressSchema(Schema):
    class Meta:
        unknown = INCLUDE

    line = fields.Str(missing=None, nullable=True, allow_none=True)
    city = fields.Str(missing=None, nullable=True, allow_none=True)
    state = fields.Str(missing=None, nullable=True, allow_none=True)
    postal_code = fields.Str(missing=None, nullable=True, allow_none=True)

    @pre_load
    def add_coordinate_if_empty(self, data, **kwargs):
        if 'coordinate' not in data:
            data['coordinate'] = RealtorCoordinateSchema().load({})
        return data


class RealtorLocationSchema(Schema):
    class Meta:
        unknown = INCLUDE

    address = fields.Nested(RealtorAddressSchema())

    @pre_load
    def add_address_if_empty(self, data, **kwargs):
        if 'address' not in data:
            data['address'] = RealtorAddressSchema().load({})
        return data


class RealtorDescriptionSchema(Schema):
    class Meta:
        unknown = INCLUDE

    lot_sqft = fields.Float(missing=None, nullable=True, allow_none=True)
    baths = fields.Float(missing=None, nullable=True, allow_none=True)
    beds = fields.Float(missing=None, nullable=True, allow_none=True)
    sqft = fields.Integer(missing=None, nullable=True, allow_none=True)
    type = fields.Str(missing=None, nullable=True, allow_none=True)


class RealtorPrimaryPhotoSchema(Schema):
    class Meta:
        unknown = INCLUDE

    href = fields.Str(missing=None, nullable=True, allow_none=True)


class RealtorPropertySchema(BasePropertySchema, Schema):
    class Meta:
        unknown = INCLUDE

    property_id = fields.Str(required=True)
    list_price = fields.Integer(missing=None, nullable=True, allow_none=True)
    permalink = fields.Str(missing=None, nullable=True)
    location = fields.Nested(RealtorLocationSchema(many=False))
    description = fields.Nested(RealtorDescriptionSchema(many=False))
    primary_photo = fields.Nested(RealtorPrimaryPhotoSchema(many=False))


    @pre_load
    def add_data_if_empty(self, data, **kwargs):
        if 'location' not in data:
            data['location'] = RealtorLocationSchema().load({})
        if 'description' not in data:
            data['description'] = RealtorDescriptionSchema().load({})
        if 'primary_photo' not in data:
            data['primary_photo'] = RealtorPrimaryPhotoSchema().load({})
        return data

    @classmethod
    def to_property_data(cls, data: dict) -> PropertyData:
        description, year_built, hoa_dues, days_on_market = None, None, None, None
        return PropertyData(
            id = data["property_id"],
            address = data["location"]["address"]["line"],
            city = data["location"]["address"]["city"],
            state = data["location"]["address"]["state"],
            zip_code = data["location"]["address"]["postal_code"],
            land_area = data["description"]["lot_sqft"] if data["description"]["lot_sqft"] else None,
            land_area_unit = "sqft",
            property_estimate_value = None,
            latitude = data["location"]["address"]["coordinate"]["lat"] if data["location"]["address"]["coordinate"]["lat"] else None,
            longitude = data["location"]["address"]["coordinate"]["lon"] if data["location"]["address"]["coordinate"]["lon"] else None,
            price = data["list_price"],
            image = data["primary_photo"]["href"] if data["primary_photo"]["href"] else None,
            bathrooms = data["description"]["baths"] if data["description"]["baths"] else None,
            bedrooms = data["description"]["beds"] if data["description"]["beds"] else None,
            property_area = data["description"]["sqft"] if data["description"]["sqft"] else None,
            external_url = "https://www.realtor.com/realestateandhomes-detail/" + data["permalink"],
            home_type = data["description"]["type"] if data["description"]["type"] else None,
            description = description,
            year_built = year_built,
            hoa_dues = hoa_dues,
            days_on_market = days_on_market,
        )
