import requests

def getResponse():
    api_key = 'API_KEY'
    response = requests.post(
        'https://offerpad.direct/api/get-properties',
        headers={'Accept': 'application/json', 'show': 'all'},
        auth=('YOURAPIKEY', api_key)
    )
    results = response.json()
    allproperties = results['results']
    return allproperties
