import pymongo
import asyncio

client = pymongo.AsyncMongoClient("mongodb://localhost:27017")
db = client["publisher_db"]
publishers_collection = db["publishers"]
books_collection = db["books"]

data = {"lista" : [] }
async def main():
    pub = await publishers_collection.insert_one({
        "name": 'Mondadori',
        "founded_year": 1907,
        "country": 'Italia'
    })
    pub_id = str(pub.inserted_id)
    await books_collection.insert_one({
        "publisher_id": pub_id,
        "name": 'Libro Mondadori',
        "year": 2024
    })






if __name__ == '__main__':
    asyncio.run(main())
