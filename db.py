# %%
from pymongo import MongoClient
import json
import pandas as pd
## MongoDB creates DB/Collection lazily.
# %%
## Update data every 5 minutes
def get_collections():
    return ['fundings', 'price', 'spot_cvd', 'future_cvd', 'open_interest', 'future_volume', 'spot_volume', 'lsur']
# collections = ['fundings', 'price', 'spot_cvd', 'future_cvd', 'open_interest', 'volume']

def getDB(remote=False):
    config = json.load(open('config.json'))
    if remote:
        client = MongoClient(config["mongo_remote_url"])
    else:
        client = MongoClient('localhost', 27017)
    db = client.Crypto
    return db

def initDB(db):
    # db.create_collection('data', timeseries={ 'timeField': 'timestamp' })
    db.create_collection('data')
    # collections = get_collections()
    # for collection in collections:
    #     if collection not in db.list_collection_names():
    #         db.create_collection(collection, timeseries={ 'timeField': 'timestamp' })
    #         print(f'Collection {collection} created.')
    #     else:
    #         print(f'Collection {collection} exists.')

def insert(db, collection, data):
    db[collection].insert_one(data)

def time_to_minutes(interval):
    if interval[-1] == 'w':
        return int(interval[:-1]) * 7 * 24 * 60
    elif interval[-1] == 'd':
        return int(interval[:-1]) * 24 * 60
    elif interval[-1] == 'h':
        return int(interval[:-1]) * 60
    elif interval[-1] == 'm':
        return int(interval[:-1])

def search(db, symbol, indicator=None, collection='data', interval='4h'):
    """
    By default 15min candles.
    """
    num_candles = time_to_minutes(interval) // 15
    result = list(db[collection].find({"symbol": symbol}).sort("timestamp", -1).limit(num_candles))
    result.reverse()
    df = pd.DataFrame(result)
    # print(df)
    df = df.set_index("timestamp")
    # print(df)
    return df




# %%
if __name__ == '__main__':
    db = getDB(remote=True)
    # initDB(db)
    df = search(db, 'BTCUSDT')
    df['price'].plot()
# %%
