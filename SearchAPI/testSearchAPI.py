# test some of the search API. See V1Search.py for a more complete CLI search tool
import TMVisionOne
import tmconfig
from datetime import datetime, timedelta  # to calculate date and time range of the search
# change your region
x = TMVisionOne.XDR('us', tmconfig.xdr_token, "Trend Micro Vision One Test.py sample")
#print("Get Active OS for the last 7 days ")
#print(x.getActiveOSinfos7d())
print("Get V1 computer Id \n")
# pick 2 endpoint names and change the code below to test in your environments and save their Id's for the other API's
print(x.getComputerId('Dev2022')) # "b30684f7-5e37-4899-9219-8ea3e7ba0b20"
print(x.getComputerId('win110johnd-7001')) #"38cb57d8-e50d-43ce-aef8-e822fb475bab"
print("Get endpoint infos \n")
print(x.getSingleEndPointInfos("b30684f7-5e37-4899-9219-8ea3e7ba0b20"))
print("Get Multiple Endpoint iformations \n")
print(x.getMultiEndPointInfos(["b30684f7-5e37-4899-9219-8ea3e7ba0b20", "38cb57d8-e50d-43ce-aef8-e822fb475bab"]))
print("************** Search Detections Test *****************\n")
qry = "endpointHostName:win110johnd-7001"
idays = 7
my_date = datetime.now() - timedelta(days=idays)
istart = str(my_date.replace(microsecond=0))
iEnd = str(datetime.today().replace(microsecond=0) + timedelta(days=1))
print(x.searchDetections(startTime=istart, endTime=iEnd,query=qry))
