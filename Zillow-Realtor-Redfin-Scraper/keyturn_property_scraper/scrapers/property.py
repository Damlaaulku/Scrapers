from dataclasses import dataclass
from typing import Optional


@dataclass
class PropertyData:
    id: str
    address: Optional[str]
    city: Optional[str]
    state: Optional[str]
    zip_code: Optional[str]
    land_area: Optional[float]
    land_area_unit: Optional[str]
    property_estimate_value: Optional[int]
    latitude: Optional[float]
    longitude: Optional[float]
    price: Optional[int]
    image: Optional[str]
    bathrooms: Optional[float]
    bedrooms: Optional[float]
    property_area: Optional[int]
    external_url: Optional[str]
    description: Optional[str]
    year_built: Optional[int]
    hoa_dues: Optional[str]
    days_on_market: Optional[int]
    home_type: Optional[str]
