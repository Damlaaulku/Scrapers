import random
import time

from redfin_custom import Redfin
from dataclasses import dataclass
from typing import Optional


@dataclass
class RedfinFields:
    id: str
    description: Optional[str]
    year_built: Optional[int]
    hoa_dues: Optional[str]
    days_on_market: Optional[int]

    @classmethod
    def get_redfin_fields(cls, property) -> dict:
        time.sleep(random.randint(100, 1500) / 1000)

        try:
            client = Redfin()
            response = client.search(property["address"])
            payloads = response['payload']
            url = payloads['exactMatch']['url']
            initial_info = client.initial_info(url)
            initpayloads = initial_info['payload']
            property_id = initpayloads['propertyId']
            below_the_fold = client.below_the_fold(property_id)
        except:
            description = None
            year_built = None
        try:
            events = below_the_fold['payload']['propertyHistoryInfo']['events'][0]
            description = events['marketingRemarks'][0]['marketingRemark']
        except:
            description = None
        try:
            basic = below_the_fold['payload']['publicRecordsInfo']['basicInfo']
            year_built = basic['yearBuilt']
        except:
            year_built = None
        try:
            listing_id = initpayloads['listingId']
            info_panel = client.info_panel(property_id, listing_id)
            main_info = info_panel['payload']['mainHouseInfo']
            hoa_info = main_info['selectedAmenities'][0]
            if hoa_info['header'] == "HOA Dues":
                hoa_dues = hoa_info['content']
            else:
                hoa_dues = ""
        except:
            hoa_dues = None
        try:
            above_the_fold = client.above_the_fold(property_id, listing_id)
            addressSection = above_the_fold["payload"]["addressSectionInfo"]
            days_on_market = addressSection["cumulativeDaysOnMarket"]
        except:
            days_on_market = None

        return cls(
            id=property["id"],
            description=description,
            year_built=year_built,
            hoa_dues=hoa_dues,
            days_on_market=days_on_market,
        )


