from oauth2client.service_account import ServiceAccountCredentials
import requests
import gspread
import json
import time

fields={"neighborhood":"","locality":"","administrative_area_level_1":"","administrative_area_level_2":"","business_status":"","current_opening_hours":"","formatted_address":"","formatted_phone_number":"","international_phone_number":"","name":"","place_id":"","rating":"","reviews":"","user_ratings_total":"","website":""}
keys=list(fields.keys())

scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
            "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name('client_services.json', scope)
client = gspread.authorize(credentials)
spreadsheet = client.open('SPREADSHEET_NAME')
worksheet = spreadsheet.worksheet("WORKSHEET_NAME_TO_READ")
cities = worksheet.col_values(1)
worksheet = spreadsheet.worksheet("WORKSHEET_NAME_TO_WRITE")
worksheet.append_row(keys)
worksheet.format('A1:GA1', {'textFormat': {'bold': True}})
GOOGLE_API_KEY='GOOGLE_API_KEY'
payload={}
headers = {}

for c in cities:
    c=c.replace(" ","%20")
    print(c)
    text_search_url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query=pawn%20shops%20in%20"+c+"%20USA&key="+ GOOGLE_API_KEY
    response_text_search = json.loads(requests.request("GET", text_search_url, headers=headers, data=payload).text)
    text_search_results = response_text_search['results']

    
    for i in text_search_results:
        place_id = i['place_id']
        place_details_url = "https://maps.googleapis.com/maps/api/place/details/json?place_id="+ place_id +"&key="+ GOOGLE_API_KEY
        response_place_details = json.loads(requests.request("GET", place_details_url, headers=headers, data=payload).text)
        result= response_place_details['result']
        address_components = result['address_components']
        for a in address_components:
            if a["types"][0] == "neighborhood":
                fields['neighborhood'] = a["long_name"]
            if a["types"][0] == "locality":
                fields['locality'] = a["long_name"]
            if a["types"][0] == "administrative_area_level_1":
                fields['administrative_area_level_1'] = a["long_name"]
            if a["types"][0] == "administrative_area_level_2":
                fields['administrative_area_level_2'] = a["long_name"]
        fields['name'] = result['name']
        fields['place_id'] = result['place_id']
        try:
            fields['business_status'] = result['business_status']
        except:
            fields['business_status'] = ""
        try:
            fields['current_opening_hours'] = str(result['current_opening_hours']['weekday_text'])
        except:
            fields['current_opening_hours'] = ""
        try:
            fields['formatted_address'] = result['formatted_address']
        except:
            fields['formatted_address'] = ""
        try:
            fields['formatted_phone_number'] = result['formatted_phone_number']
        except:
            fields['formatted_phone_number'] = ""
        try:
            fields['international_phone_number'] = str(result['international_phone_number']).replace("+","")
        except:
            fields['international_phone_number'] = ""
        try:
            fields['rating'] = result['rating']
        except:
            fields['rating'] = ""
        reviewsList = []
        try:
            reviews=result['reviews']
            for r in reviews:
                reviewsDict={"author_name":"","rating":"","relative_time_description":"","text":""}
                reviewsDict["author_name"]=r["author_name"]
                reviewsDict["rating"]=r["rating"]
                reviewsDict["relative_time_description"]=r["relative_time_description"]
                reviewsDict["text"]=r["text"]
                reviewsList.append(reviewsDict)
            fields['reviews']=str(reviewsList)
        except:
            fields['reviews']=""
        try:
            fields['user_ratings_total'] = result['user_ratings_total']
        except:
            fields['user_ratings_total'] = ""
        try:
            fields['website'] = result['website']
        except:
            fields['website'] = ""
        if fields['administrative_area_level_1'] == 'Florida' or fields['administrative_area_level_1'] == 'Georgia' or fields['administrative_area_level_1'] == 'Texas':
            values=list(fields.values())
            worksheet.append_row(values, value_input_option='USER_ENTERED')
        else:
            continue
        time.sleep(1)
    time.sleep(2)
