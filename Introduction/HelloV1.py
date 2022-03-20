#HelloV1.py
# The purpose of this very basic example is to test your dev environment (PyCharm, Python 3.7+)
# Add requests from PyCharm or Add via pip3 install requests
import requests
import json
xdr_token = 'Put-your-api-token-here'
# get your region from https://automation.trendmicro.com/xdr/Guides/Regional-Domains
region = "https://api.xdr.trendmicro.com"
header = {'Authorization': 'Bearer ' + xdr_token, 'Content-Type': 'application/json;charset=utf-8'}
url_path = '/v2.0/xdr/dmm/models'
query_params = {}
r = requests.get(region + url_path, params=query_params, headers=header)
# if the region or any other network issue happen, you won't get here, untrapped error :)
print(r.status_code)
if 'application/json' in r.headers.get('Content-Type', ''):
    print(json.dumps(r.json(), indent=4))
else:
    print(r.text)
