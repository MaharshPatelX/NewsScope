import json
import pymongo


client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client['newsdata']
collection = db['news']

with open('data/news.json', 'r') as file:
    file_data = json.load(file)

for x in file_data:
	del x['_id']
	collection.insert_one(x)

print("Data uploaded successfully to MongoDB.")
