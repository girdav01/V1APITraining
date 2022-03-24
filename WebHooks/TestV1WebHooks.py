# TestV1WebHooks
import tmconfig
import TMVisionOne
import json
# application name = name of the script minus .py. Add version if you want
appname = __file__.rsplit("/", 1)[1].split('.')[0]
# this sample will use a demo V1 API wrapper class. Note this is demo code not for production.
x = TMVisionOne.XDR('us', tmconfig.xdr_token, appname)
print("Listing WebHooks")
print(x.queryHooks())

print("Creating a WebHook")
url="https://d683-135-19-86-136.ngrok.io/webhook?verify_token=5f104165147defc18bf868eb95c2ad61bfdd6f7967490166"
print(x.createHook(url))

print("Testing the trigger webhook api")
data = {
    "text": {'workbenchId': 'WB-10797-20210506-00013', 'modelName': '[Threat Hunting] Suspicious WMI Executing Local Or Remote Process', 'completedTime': '2021-05-06T03:46:43Z', 'priorityScore': 47, 'severity': 'medium', 'desktopCount': 1, 'serverCount':
0, 'accountCount': 2, 'emailAddressCount': 0, 'link': 'https://portal.xdr.trendmicro.com/index.html#/workbench?workbenchId=WB-10797-20210506-00013&ref=a88b7dcd1a9e3e17770bbaa6d7515b31a2d7e85d', 'modelId': '5a7e6c80-4add-4641-9d72-4efaae0254d2'}
}
body = json.dumps(data)
print(x.triggerHook("workbench",data)) # for instant test

#print("Testing the Update Webhook API")
#x.updateHook('webhookId',data)
#print(x.queryHooks()) # show changes
#print("Testing the Delete Webhook API")
#print (x.deleteHook('webhookId'))
#print(x.queryHooks()) # show changes