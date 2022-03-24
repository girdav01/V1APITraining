import requests
import json
import tmconfig
appname = __file__
url_base = tmconfig.region["us"]
token = tmconfig.xdr_token
url_path = '/v2.0/xdr/threatintel/suspiciousObjects'
query_params = {'skipToken': "",
                    'limit': 10,
                    'type': "ip",
                    'scanAction': "block",
                    'startTime': "2021-08-17-T00:00:01Z",
                    'contentFilter': ""
                }


headers = {'Authorization': 'Bearer ' + token , 'Content-Type': 'application/json;charset=utf-8',
           'User-Agent': appname}

r = requests.get(url_base + url_path, params=query_params, headers=headers)

print(r.status_code)
if 'application/octet-stream' in r.headers.get('Content-Type', ''):
    print(json.dumps(r.json(), indent=4))
else:
    print(r.text)