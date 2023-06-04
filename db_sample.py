# %%
from pymongo import MongoClient
client = MongoClient('localhost', 27017)


# %%
db = client.test_database
# %%
db
# %%
collection = db.test_collection
# %%
import datetime
post = {
    "author": "Mike",
    "text": "First post",
    "date": datetime.datetime.utcnow()
}
# %%
posts = db.posts
# %%
post_id = posts.insert_one(post).inserted_id
post_id
# %%
db.list_collection_names()
# %%
