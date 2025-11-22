import tornado.web
import tornado.ioloop
import asyncio
import json

from bson import ObjectId

from setup_database import data, db, publishers_collection, books_collection



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

    async def post(self):

        data1 = json.loads(self.request.body)

        nuovo_editore = {
            "name": data1["name"],
            "founded_year": data1["founded_year"],
            "country": data1["country"]
        }

        await publishers_collection.insert_one(nuovo_editore)

        self.set_header("Content-Type", "application/json")



class PublisherCasaEditrice(tornado.web.RequestHandler):

    async def get(self, id):
        result = [editore for editore in data["lista"] if str(editore["_id"]) == id]

        self.set_header("Content-Type", "application/json")
        self.write(json.dumps({"lista": result}))

    async def put(self, id):
        data1 = json.loads(self.request.body)

        editore_Aggiornato = {
            "name": data1["name"],
            "founded_year": data1["founded_year"],
            "country": data1["country"]
        }

        await publishers_collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": editore_Aggiornato}
        )

        self.set_header("Content-Type", "application/json")

    async def delete(self, id):
        await publishers_collection.delete_one({"_id": ObjectId(id)})
        await books_collection.delete_many({"publisher_id": id})

class PublisherBooks(tornado.web.RequestHandler):

    async def get(self, id_editore):
        genre = self.get_query_argument("genre", None)
        author = self.get_query_argument("author", None)
        title = self.get_query_argument("title", None)

        query = {"publisher_id": id_editore}

        if genre:
            query["genre"] = genre
        if author:
            query["author"] = author
        if title:
            query["title"] = title

        result = await books_collection.find(query).to_list()

        for libro in result:
            libro["_id"] = str(libro["_id"])

        self.set_header("Content-Type", "application/json")
        self.write(json.dumps({"lista": result}))

    async def post(self, id_editore):
        data1 = json.loads(self.request.body)

        nuovo_libro = {
        "publisher_id": id_editore,
        "title": data1["title"],
        "author": data1["author"],
        "genre": data1["genre"],
        "year": 2008
        }
        await books_collection.insert_one(nuovo_libro)

        self.set_header("Content-Type", "application/json")


class BookHandler(tornado.web.RequestHandler):
    async def get(self, id_editore, id_libro):
        r = await books_collection.find_one(
            {
            "_id": ObjectId(id_libro),
            "publisher_id": id_editore,
            }
        )
        if r:
            r["_id"] = str(r["_id"])
            self.write(json.dumps({"lista": r}))

    async def put(self, id_editore, id_libro):
        data = json.loads(self.request.body)

        aggiorna_libro = {
        "publisher_id": id_editore,
        "title": data["title"],
        "author": data["author"],
        "genre": data["genre"],
        "year": 2008
        }

        r = await books_collection.update_one(
            {
            "_id": ObjectId(id_libro),
            "publisher_id": id_editore,
            },
            {"$set":aggiorna_libro}
        )

    async def delete(self, id_editore, id_libro ):
        await books_collection.delete_one(
            {
            "_id": ObjectId(id_libro),
            "publisher_id": id_editore,
            })


def make_app():
    return tornado.web.Application([
        (r"/publishers", Publisher),
        (r"/publishers/([0-9a-z]+)", PublisherCasaEditrice),
        (r"/publishers/([0-9a-z]+)/books", PublisherBooks),
        (r"/publishers/([0-9a-z]+)/books/([0-9a-z]+)", BookHandler),

    ])



async def main(shutdown_event):
    cursor = publishers_collection.find({})
    async for documento in cursor:
        documento["_id"] = str(documento["_id"])
        data["lista"].append(documento)

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
