from urllib.parse import urlencode
import httpx
import time


job_listing = {"company":'', "job_URL":'', "job_title":'', "company_size":'', "company_URL":'', "dm_name":'', "dm_title":'', "dm_email":'', "salary":'', "stack":'', "job_description":''}

params = {
    "x-algolia-agent": "Algolia for JavaScript (4.14.2); Browser (lite)",
    "x-algolia-api-key": "7a1d0ebc0d0e9ba3dc035fc09729f2a8",
    "x-algolia-application-id": "OQUBRX6ZEQ"
}
search_url = "https://oqubrx6zeq-dsn.algolia.net/1/indexes/*/queries?" + urlencode(params)

page_num = 0
search_data = {
    "requests": [
        {
            "indexName": "live_jobs",
            "params": "facetFilters=%5B%5B%22job_type%3AFull-time%22%5D%2C%5B%22category%3ASoftware%20Development%22%5D%5D&facets=%5B%22tags%22%2C%22job_type%22%2C%22company_name%22%2C%22locations%22%2C%22category%22%5D&maxValuesPerFacet=1000&page=" + str(page_num) + "&query=&tagFilters="
        },
        {
            "indexName": "live_jobs",
            "params": "analytics=false&clickAnalytics=false&facetFilters=%5B%5B%22category%3ASoftware%20Development%22%5D%5D&facets=job_type&hitsPerPage=0&maxValuesPerFacet=1000&page=0&query="
        },
        {
            "indexName": "live_jobs",
            "params": "analytics=false&clickAnalytics=false&facetFilters=%5B%5B%22job_type%3AFull-time%22%5D%5D&facets=%5B%22category%22%5D&hitsPerPage=0&maxValuesPerFacet=1000&page=0&query="
        }
    ]
}
response = httpx.post(search_url, json=search_data)
data = response.json()["results"][0]["hits"]

while len(data)>0:
    for job in data:
        if "Manager" in job["title"] or "Director" in job["title"] or "VP" in job["title"]:
            continue
        else:
            try:
                job_listing["company"] = job["company_name"]
            except:
                job_listing["company"] = ""
            try:
                job_listing["job_URL"] = job["url"]
            except:
                job_listing["job_URL"] = ""
            try:
                job_listing["job_title"] = job["title"]
            except:
                job_listing["job_title"] = ""
            try:
                if job["salary"] == False:
                    job_listing["salary"] = ""
                else:
                    job_listing["salary"] = job["salary"]
            except:
                job_listing["salary"] = ""
            try:
                job_listing["company_URL"] = job["company_url"]
            except:
                job_listing["company_URL"] = ""
            try:
                job_listing["job_description"] = job["_source"]["description"]
            except:
                job_listing["job_description"] = ""
            values=list(job_listing.values())
            print(values)
            time.sleep(3)
    page_num +=1
    search_data = {
        "requests": [
            {
                "indexName": "live_jobs",
                "params": "facetFilters=%5B%5B%22job_type%3AFull-time%22%5D%2C%5B%22category%3ASoftware%20Development%22%5D%5D&facets=%5B%22tags%22%2C%22job_type%22%2C%22company_name%22%2C%22locations%22%2C%22category%22%5D&maxValuesPerFacet=1000&page=" + str(page_num) + "&query=&tagFilters="
            },
            {
                "indexName": "live_jobs",
                "params": "analytics=false&clickAnalytics=false&facetFilters=%5B%5B%22category%3ASoftware%20Development%22%5D%5D&facets=job_type&hitsPerPage=0&maxValuesPerFacet=1000&page=0&query="
            },
            {
                "indexName": "live_jobs",
                "params": "analytics=false&clickAnalytics=false&facetFilters=%5B%5B%22job_type%3AFull-time%22%5D%5D&facets=%5B%22category%22%5D&hitsPerPage=0&maxValuesPerFacet=1000&page=0&query="
            }
        ]
    }
    response = httpx.post(search_url, json=search_data)
    data = response.json()["results"][0]["hits"]
