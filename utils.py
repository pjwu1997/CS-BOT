# %%
from datetime import datetime
import requests
import pandas as pd
from db import getDB, insert, get_collections, search
from get_all_pairs import get_all_pair

future_base_url = "https://fapi.binance.com"
spot_base_url = "https://api.binance.com"

def get_all_symbols():
    future_base_url = future_base_url + "/fapi/v1/exchangeInfo"
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    result = []
    for item in response.json()["symbols"]:
        if item["symbol"][-4:] == 'USDT':
            result.append(item["symbol"])
    return result

def update(timestamp):
    symbols = get_all_pair()
    collections = get_collections()
    db = getDB(remote=True)
    for symbol in symbols:
        data = {
            "fundings": None,
            "open_interest": None,
            "price": None,
            "spot_cvd": None,
            "future_cvd": None,
            "lsur": None,
            "future_volume": None,
            "spot_volume": None,
        }
        params = {'symbol': symbol}
        for util in [get_open_interest, get_price, get_spot_cvd, get_future_cvd, get_lsur]:
            try:
                data.update(util(symbol))
            except:
                print('data not found for ' + symbol)
        # for key, value in data.items():
        #     insert_data = {
        #         "symbol": symbol,
        #         "timestamp": timestamp,
        #         key: value,
        #     }
        #     insert(db, key, insert_data)
        data["symbol"] = symbol
        data["timestamp"] = timestamp
        insert(db, 'data', data)

    

# def get_funding(symbol):
#     url = "https://fapi.binance.com/fapi/v1/premiumIndex"
#     params = {'symbol': symbol}
#     res = requests.get(url, params=params)
#     return res.json()["lastFundingRate"]

def get_open_interest(symbol):
    url = future_base_url + '/fapi/v1/openInterest'
    params = {'symbol': symbol}
    res = requests.get(url, params=params).json()
    data = {
        "open_interest": float(res["openInterest"]),
    }
    return data

def get_price(symbol):
    url = future_base_url + "/fapi/v1/premiumIndex"
    params = {'symbol': symbol}
    res = requests.get(url, params=params).json()
    data = {
        "price": float(res["markPrice"]),
        "fundings": float(res["lastFundingRate"]),
    }
    return data

def get_future_cvd(symbol, period='15m', limit=1):
    url = future_base_url + '/futures/data/takerlongshortRatio'
    params = {'symbol': symbol, 'period': period, 'limit': limit}
    res = requests.get(url, params=params).json()[0]
    data = {
        "future_cvd": float(res["buyVol"]) - float(res["sellVol"]),
        "future_volume": float(res["buyVol"]) + float(res["sellVol"]),
    }
    return data

def get_spot_cvd(symbol, period='15m', limit=1):
    url = spot_base_url + '/api/v3/klines'
    params = {'symbol': symbol, 'interval': period, 'limit': limit}
    res = requests.get(url, params=params).json()
    data = {
        "spot_cvd": float(res[0][-3]) - float(res[0][-2]) / float(res[0][2]),
        "spot_volume": float(res[0][7]) / float(res[0][2]),
    }
    return data

def get_lsur(symbol, period='15m', limit=1):
    url = future_base_url + '/futures/data/globalLongShortAccountRatio'
    params = {'symbol': symbol, 'period': period, 'limit': limit}
    res = requests.get(url, params=params).json()[0]
    data = {
        "lsur": float(res["longShortRatio"]),
    }
    return data

# %%
