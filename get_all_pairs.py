# %%
import requests

def get_all_pair():
    url = "https://fapi.binance.com/fapi/v1/exchangeInfo"

    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    result = []
    for item in response.json()["symbols"]:
        result.append(item["symbol"])

    return result
