import tornado.web
import tornado.ioloop
import asyncio
import json
import pymongo


data = {"lista": []}

client = pymongo.AsyncMongoClient("mongodb://localhost:27017")
db = client["publisher_db"]
publishers_collection = db["publishers"]

async def popola_data():
    cursor = publishers_collection.find({})
    async for documento in cursor:
        documento["_id"] = str(documento["_id"])
        data["lista"].append(documento)


asyncio.run(popola_data())



class Publisher(tornado.web.RequestHandler):

    async def get(self):
        name = self.get_query_argument("name", None)
        country = self.get_query_argument("country", None)

        result = data["lista"]

        if name:
            result = [p for p in result if p["name"] == name]
        if country:
            result = [p for p in result if p["country"] == country]

        self.set_header("Content-Type", "application/json")
        self.write(json.dumps({"lista": result}))



def make_app():
    return tornado.web.Application([
        (r"/publishers", Publisher),
    ])


async def main(shutdown_event):
    app = make_app()
    app.listen(8888)
    print("Server attivo su http://localhost:8888/publishers")
    await shutdown_event.wait()


if __name__ == "__main__":
    shutdown_event = asyncio.Event()
    try:
        asyncio.run(main(shutdown_event))
    except KeyboardInterrupt:
        shutdown_event.set()
