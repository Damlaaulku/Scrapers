import requests
import time

job_listing = {"company":'', "job_URL":'', "job_title":'', "company_size":'', "company_URL":'', "dm_name":'', "dm_title":'', "dm_email":'', "salary":'', "stack":'', "job_description":''}

url="https://www.workingnomads.com/jobsapi/job/_search?sort=expired:asc,premium:desc,pub_date:desc&_source=company,category_name,description,locations,location_base,salary_range,salary_range_short,number_of_applicants,instructions,id,external_id,slug,title,pub_date,tags,source,apply_url,premium,expired,use_ats,position_type&size=500&from=0&q=(category_name.raw:%22Marketing%22)"

headers = {
    'authority': 'www.workingnomads.com',
    'method': 'GET',
    'path': '/jobsapi/job/_search?sort=expired:asc,premium:desc,pub_date:desc&_source=company,category_name,description,locations,location_base,salary_range,salary_range_short,number_of_applicants,instructions,id,external_id,slug,title,pub_date,tags,source,apply_url,premium,expired,use_ats,position_type&size=500&from=0&q=(category_name.raw:%22Marketing%22)',
    'scheme': 'https',
    'accept': 'application/json, text/plain, */*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'no-cache',
    'cookie': 'subscriber_source=""; subscriber_utm_source=""; subscriber_utm_medium=""; subscriber_utm_campaign=""; _ga=GA1.2.218669659.1673987688; _gid=GA1.2.537558851.1673987688',
    'pragma': 'no-cache',
    'referer': 'https://www.workingnomads.com/remote-development-jobs',
    'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': "Windows",
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
}
response = requests.get(url=url,headers=headers)
data = response.json()["hits"]["hits"]

for job in data:
    if not job["_source"]["expired"]:
        if "VP" in job["_source"]["title"] or "Head of" in job["_source"]["title"] or "Product" in job["_source"]["title"]:
            continue
        else:
            try:
                job_listing["company"] = job["_source"]["company"]
            except:
                job_listing["company"] = ""
            try:
                job_listing["job_URL"] = job["_source"]["apply_url"]
            except:
                job_listing["job_URL"] = ""
            try:
                job_listing["job_title"] = job["_source"]["title"]
            except:
                job_listing["job_title"] = ""
            try:
                job_listing["salary"] = job["_source"]["salary_range"]
            except:
                job_listing["salary"] = ""
            try:
                job_listing["job_description"] = job["_source"]["description"]
            except:
                job_listing["job_description"] = ""
            values=list(job_listing.values())
            print(values)
            time.sleep(3)
