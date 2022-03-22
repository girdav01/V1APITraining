'''
Config file for some of Trend Micro Vision One Scripts.
XDR Product Manager Team, November 2020
Do not share your api keys in public github
Last update March 2022
Get your token from your XDR Administrator, in Vision One Console under Account Management.
'''
xdr_token = 'Put your API token here'

'''
Region            FQDN
Australia         api.au.xdr.trendmicro.com
European Union    api.eu.xdr.trendmicro.com
india             api.in.xdr.trendmicro.com
Japan             api.xdr.trendmicro.co.jp
Singapore         api.sg.xdr.trendmicro.com
United States     api.xdr.trendmicro.com

for an update list : https://automation.trendmicro.com/xdr/Guides/Regional-Domains

please update region dictionary
'''
region = {'au': 'https://api.au.xdr.trendmicro.com', 'eu': 'https://api.eu.xdr.trendmicro.com',
          'in': 'https://api.in.xdr.trendmicro.com', 'jp': 'https://api.xdr.trendmicro.co.jp',
          'sg': 'https://api.sg.xdr.trendmicro.com', 'us': 'https://api.xdr.trendmicro.com'}
