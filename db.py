# %%
from pymongo import MongoClient
## MongoDB creates DB/Collection lazily.
# %%
## Update data every 5 minutes
def get_collections():
    return ['fundings', 'price', 'spot_cvd', 'future_cvd', 'open_interest', 'future_volume', 'spot_volume', 'lsur']
# collections = ['fundings', 'price', 'spot_cvd', 'future_cvd', 'open_interest', 'volume']

def getDB():
    client = MongoClient('localhost', 27017)
    db = client.crypto_data
    return db

def initDB(db):
    collections = get_collections()
    for collection in collections:
        if collection not in db.list_collection_names():
            db.create_collection(collection, timeseries={ 'timeField': 'timestamp' })
            print(f'Collection {collection} created.')
        else:
            print(f'Collection {collection} exists.')

def insert(db, collection, data):
    db[collection].insert_one(data)

# %%
if __name__ == '__main__':
    db = getDB()
    initDB(db)
# %%
