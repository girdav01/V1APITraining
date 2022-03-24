# The purpose of this python script is to test your web server with post  (with or without ngrok) before registering
# to Vision One Web Hook
import requests
import json

#Change this url to fit your hook
url = "https://d683-135-19-86-136.ngrok.io/webhook?verify_token=5f104165147defc18bf868eb95c2ad61bfdd6f7967490166"

header = {'Content-Type': 'application/json', 'User-Agent': 'post test'}

# this wathever json to simulate Webhook json payload
data2 = {
    "text": "From sendPosttes.py ",
	"attachments": [
		{
			"blocks": [
				{
					"type": "section",
					"text": {
						"type": "plain_text",
						"text": "this is a test from David using attachments json format"
					}
				}
			]
		}
	]
}

body = json.dumps(data2)
r = requests.post(url, headers=header, data=body)
print(str(r.status_code))
print(json.dumps(r.json(), indent=4))

