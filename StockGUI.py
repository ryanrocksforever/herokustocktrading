import requests
import json

uponly = False
global beststock
url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/market/get-trending-tickers"

querystring = {"region": "US"}

headers = {
    'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com",
    'x-rapidapi-key': "714ff4f6eamsh9bc6892019abf3bp1df1b1jsn082fce7a6b7d"
}

response = requests.request("GET", url, headers=headers, params=querystring)

# print(response.text)

cccccccc