import requests
import json
import tmconfig
import base64

filename = "c:\\code\\main.class"
url_base = 'https://api.xdr.trendmicro.com'
url_path = '/v2.0/xdr/sandbox/file'

token = tmconfig.xdr_token

headers = {'Authorization': 'Bearer ' + token}
query_params = {}
sample_password = 'infected'
#data = {'archivePassword': base64.b64encode(sample_password.encode('ascii')).decode('ascii')}
#data = {'documentPassword': '','archivePassword': ''}
#data = {'documentPassword': base64.b64encode(sample_password.encode('ascii')).decode('ascii')}
data = {}

# for zip 'application/x-zip-compressed'
files = {'file': ('main.class', open(filename, 'rb'), 'application/octet-stream')}

r = requests.post(url_base + url_path,headers=headers, data=data, files=files)

print(r.status_code)
if 'application/json' in r.headers.get('Content-Type', ''):
    print(json.dumps(r.json(), indent=4))
else:
    print(r.text)