'''
GeneralV1.py
The purpose of this very basic example is to test some general purpose API's

'''
import requests
import json
import tmconfig # to get the token and region url
region = tmconfig.region['us']
appname = 'GeneralV1.py'
header = {'Authorization': 'Bearer ' + tmconfig.xdr_token, 'Content-Type': 'application/json;charset=utf-8',
          'User-Agent': appname}

# wrapper on requests get
def get(url_path, query_params):
    r = requests.get(region + url_path, params=query_params, headers=header)
    print(r.status_code)
    if 'application/json' in r.headers.get('Content-Type', ''):
        return json.dumps(r.json(), indent=4)
    raise RuntimeError(f'Request unsuccessful (GET {url_path}):'
                       f' {r.status_code} {r.text}')

# wrapper on requests post
def post(url_path, query_params, body):
    r = requests.post(region + url_path, params=query_params, headers=header, data=body)
    if ((200 == r.status_code) and ('application/json' in r.headers.get('Content-Type', ''))):
        return r.json()
    raise RuntimeError(f'Request unsuccessful (POST {url_path}):'
                       f' {r.status_code} {r.text}')

# Wrapper for requests delete
def delete(url_path, query_params):
    r = requests.delete(region + url_path, params=query_params, headers=header)
    print(r.status_code)
    if 'application/json' in r.headers.get('Content-Type', ''):
        return r.json()
    raise RuntimeError(f'Request unsuccessful (DELETE {url_path}):'
                        f' {r.status_code} {r.text}')

# wrapper on requests put
def put(url_path, query_params, body):
    r = requests.put(region + url_path, params=query_params, headers=header, data=body)
    if ((200 == r.status_code) and ('application/json' in r.headers.get('Content-Type', ''))):
        return r.json()
    raise RuntimeError(f'Request unsuccessful (PUT {url_path}):'
                       f' {r.status_code} {r.text}')

##### Vision One version 2.0 API

#Deletes an account from the XDR service platform
def deleteaccount(email):
    url_path = '/v2.0/xdr/portal/accounts/{email}'
    url_path = url_path.format(**{'email': email})
    query_params = {}
    return delete(url_path, query_params)

# Creates a SAML or local account
def createaccount(email, firstName, lastName):
    # note that we don't test other roles than Analyst and we hardcoded type 0 = local
    #  and we hardcoded autorization 3 (UI + API), this is just an example
    url_path = '/v2.0/xdr/portal/accounts/{email}'
    url_path = url_path.format(**{'email': email})
    query_params = {}
    data = {'type': 0,
            'firstName': firstName,
            'lastName': lastName,
            'enabled': True,
            'description': 'Test account',
            'token': tmconfig.xdr_token,
            'authorization': 3,
            'role': 'Analyst'
            }
    body = json.dumps(data)
    return post(url_path, query_params, body)

#Generates an authentication token for an account with API access
def generateToken(email):
    url_path = '/v2.0/xdr/portal/accounts/{email}/tokens'
    url_path = url_path.format(**{'email': email})
    query_params = {}
    return get(url_path, query_params)

#Deletes the authentication token of an account with API access
def deleteToken(email):
    url_path = '/v2.0/xdr/portal/accounts/{email}/tokens'
    url_path = url_path.format(**{'email': email})
    query_params = {}
    return delete(url_path, query_params)

#Configures the account password using the link in the verification message
def setPassword(email, password):
    url_path = '/v2.0/xdr/portal/accounts/{email}/passwords'
    url_path = url_path.format(**{'email': email})
    query_params = {}
    data = {'type': 0,
            'password': password,
            'token': tmconfig.xdr_token
            }
    body = json.dumps(data)
    return put(url_path, query_params)

#Sends a verification message with a link to a password configuration screen
def SendAccountVerif(email):
    url_path = '/v2.0/xdr/portal/accounts/{email}/passwords/sendEmails'
    url_path = url_path.format(**{'email': email})
    query_params = {}
    body = ''
    return post(url_path, query_params, body)

#Retrieves the status (enabled or disabled) of two-factor authentication for local accounts
def get2faStatus():
    url_path = '/v2.0/xdr/portal/accounts/mfa'
    query_params = {}
    return get(url_path, query_params)

#Retrieves a list of roles that users can select when configuring accounts
def listRoles():
    url_path = '/v2.0/xdr/portal/accounts/roles'
    query_params = {}
    return get(url_path, query_params)

#Retrieves a list of roles used in company accounts and their corresponding permissions
def listUsedRoles():
    url_path = '/v2.0/xdr/portal/roles'
    query_params = {}
    return get(url_path, query_params)

#Retrieves the permissions of a specific role for all XDR features
def getPermissions(role):
    url_path = '/v2.0/xdr/portal/roles/{role}/permissions'
    url_path = url_path.format(**{'role': role})
    query_params = {}
    return get(url_path, query_params)

#Retrieves the permissions of all roles for all XDR features
def getPermissionsAll():
    url_path = '/v2.0/xdr/portal/roles/permissions'
    query_params = {}
    return get(url_path, query_params)


#Retrieves a list of log entries that match specified criteria
def searchAuditLogs(pageIndex=1, pageSize=20, period=30, accessType=0,
                    categories="01", detail='',sort='DESC'):
    #categories = "01|02|03|04|05|06|07|08|09|0c|0d|11"
    url_path = '/v2.0/xdr/portal/auditLog/search'

    data = {'pageIndex': pageIndex,
            'pageSize': pageSize,
            'period': period,
            'accessType': accessType,
            'categories': categories,
            'detail': detail,
            'sort': sort
            }

    query_params = json.dumps(data)

    return get(url_path, query_params)

#Retrieves a list of log entries that match specified criteria
def exportAuditLogs(pageIndex=1, pageSize=20, period=30, accessType=0,
                    categories='11', detail='david',sort='DESC'):
    #categories = "01|02|03|04|05|06|07|08|09|0c|0d|11"
    url_path = '/v2.0/xdr/portal/auditLog/search'
    data = {'pageIndex': pageIndex,
            'pageSize': pageSize,
            'period': period,
            'accessType': accessType,
            'categories': categories,
            'detail': detail,
            'sort': sort
            }
    query_params = json.dumps(data)

    return get(url_path, query_params)

email = 'email@email.com' # replace by an email that never being used with Vision One
#print(createaccount(email, 'test first name', 'test last name'))
#print(deleteaccount(email))
#print(generateToken(email))
#print(listRoles())
#print(listUsedRoles())
#print(getPermissions('Analyst'))
#print(getPermissionsAll())
#print(get2faStatus())
print(searchAuditLogs())
print(exportAuditLogs(1,20,30, 0,categories='11', detail='david',sort='ASC'))
