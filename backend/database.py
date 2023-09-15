# https://pymongo.readthedocs.io/en/stable/tutorial.html
# https://learn.mongodb.com/learn/course/mongodb-crud-operations-in-python/conclusion/learn?page=2

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import pprint, certifi


uri = "mongodb+srv://changlin:chatbot@cluster0.vpvr7e8.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'), tlsCAFile=certifi.where())


# # database
db = client.chatbot_database
# a collection is a group of documents, like table
history_collection = db.history_collection
feedback_collection = db.feedback_collection
# lazy execution: Collections and databases are created when the first document is inserted into them.

# for testing
import datetime
post = {
    "author": "BIKE",
    "text": "manually inserted data not real",
    "chat_history": [{"question":"what is delamination", "answer":"this is the mito"}, {"question":"test second", "answer":"second answer"}]
    }
# native Python types (like datetime.datetime instances) which will be automatically converted to and from the appropriate BSON types.

# insert
posts = db.posts
post_id = posts.insert_one(post).inserted_id # auto generated as primary key
print(post_id)

print(db.list_collection_names())


# query using find_one
# db = client.chatbot_database
# posts = db.posts
# pprint.pprint(posts.find_one({"author": "Mike"}))

# client.close()
