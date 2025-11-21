
db = client["publisher_db"]
publishers_collection = db["publishers"]
books_collection = db["books"]

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

await main()

cursor = publishers_collection.find({})
async for documento in cursor:
    documento["_id"] = str(documento["_id"])
    data["lista"].append(documento)