import requests
import json
import tmconfig
appname = __file__
url_base = tmconfig.region["us"]
token = tmconfig.xdr_token
url_path = '/v2.0/xdr/threatintel/suspiciousObjects'
query_params = {}
body = '''
{
    "data": [
        {
            "type": "domain",
            "value": "restcdn.com",
            "description": "CTF example",
            "scanAction": "block",
            "riskLevel": "high",
            "expiredDay": "30"
        }
    ]
}
'''
headers = {'Authorization': 'Bearer ' + token , 'Content-Type': 'application/json;charset=utf-8',
           'User-Agent': appname}

r = requests.post(url_base + url_path, params=query_params, headers=headers, data=body)

print(r.status_code)
if 'application/json' in r.headers.get('Content-Type', ''):
    print(json.dumps(r.json(), indent=4))
else:
    print(r.text)
