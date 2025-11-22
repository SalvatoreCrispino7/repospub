import subprocess
import json
import time


# Funzione per recuperare tutti i publisher dal database
def get_publishers_from_db():
    result = subprocess.run(
        ["curl", "http://localhost:8888/publishers"],
        capture_output=True, text=True
    )
    response = json.loads(result.stdout)

    # Debug: stampa la risposta per capire il formato
    print(f"Publishers data: {response}")

    # Accesso alla lista dei publisher all'interno della chiave 'lista'
    publishers = response.get('lista', [])

    return publishers


# Funzione per creare nuovi publisher
def test_create_publisher():
    publisher_data = [
        {
            "name": "Publisher One",
            "founded_year": 1990,
            "country": "USA"
        },
        {
            "name": "Publisher Two",
            "founded_year": 1980,
            "country": "UK"
        },
        {
            "name": "Publisher Three",
            "founded_year": 2000,
            "country": "Canada"
        }
    ]

    for publisher in publisher_data:
        result = subprocess.run(
            [
                "curl", "-X", "POST", "http://localhost:8888/publishers",
                "-H", "Content-Type: application/json",
                "-d", json.dumps(publisher)
            ],
            capture_output=True, text=True
        )
        print(f"POST /publishers result for {publisher['name']}:")
        print(result.stdout)


# Funzione per recuperare tutti i libri di un publisher
def get_books_for_publisher(publisher_id):
    result = subprocess.run(
        ["curl", f"http://localhost:8888/publishers/{publisher_id}/books"],
        capture_output=True, text=True
    )
    books = json.loads(result.stdout)
    return books


# Funzione per creare libri per un publisher specifico
def test_create_books():
    book_data = [
        {
            "title": "Book One",
            "author": "Author A",
            "genre": "Fiction"
        },
        {
            "title": "Book Two",
            "author": "Author B",
            "genre": "Non-Fiction"
        },
        {
            "title": "Book Three",
            "author": "Author C",
            "genre": "Fantasy"
        }
    ]

    publishers = get_publishers_from_db()

    for publisher in publishers:
        if isinstance(publisher, dict) and "_id" in publisher:  # Controllo se publisher è un dizionario con "_id"
            publisher_id = publisher["_id"]
        else:
            print("Formato publisher non valido:", publisher)
            continue

        for book in book_data:
            result = subprocess.run(
                [
                    "curl", "-X", "POST", f"http://localhost:8888/publishers/{publisher_id}/books",
                    "-H", "Content-Type: application/json",
                    "-d", json.dumps(book)
                ],
                capture_output=True, text=True
            )
            print(f"POST /publishers/{publisher_id}/books result for {book['title']}:")
            print(result.stdout)


# Funzione per aggiornare un libro di un publisher
def test_update_book():
    book_update_data = {
        "title": "Updated Book Title",
        "author": "Updated Author Name",
        "genre": "Updated Genre"
    }

    publishers = get_publishers_from_db()

    for publisher in publishers:
        if isinstance(publisher, dict) and "_id" in publisher:
            publisher_id = publisher["_id"]
        else:
            print("Formato publisher non valido:", publisher)
            continue

        books = get_books_for_publisher(publisher_id)

        for book in books:
            if isinstance(book, dict) and "_id" in book:
                book_id = book["_id"]
            else:
                print("Formato libro non valido:", book)
                continue

            result = subprocess.run(
                [
                    "curl", "-X", "PUT", f"http://localhost:8888/publishers/{publisher_id}/books/{book_id}",
                    "-H", "Content-Type: application/json",
                    "-d", json.dumps(book_update_data)
                ],
                capture_output=True, text=True
            )
            print(f"PUT /publishers/{publisher_id}/books/{book_id} result:")
            print(result.stdout)


# Funzione per eliminare un libro di un publisher
def test_delete_book():
    publishers = get_publishers_from_db()

    for publisher in publishers:
        if isinstance(publisher, dict) and "_id" in publisher:
            publisher_id = publisher["_id"]
        else:
            print("Formato publisher non valido:", publisher)
            continue

        books = get_books_for_publisher(publisher_id)

        for book in books:
            if isinstance(book, dict) and "_id" in book:
                book_id = book["_id"]
            else:
                print("Formato libro non valido:", book)
                continue

            result = subprocess.run(
                [
                    "curl", "-X", "DELETE", f"http://localhost:8888/publishers/{publisher_id}/books/{book_id}",
                ],
                capture_output=True, text=True
            )
            print(f"DELETE /publishers/{publisher_id}/books/{book_id} result:")
            print(result.stdout)


# Funzione per aggiornare i dettagli di un publisher
def test_update_publisher():
    publisher_update_data = {
        "name": "Updated Publisher",
        "founded_year": 1995,
        "country": "Canada"
    }

    publishers = get_publishers_from_db()

    for publisher in publishers:
        if isinstance(publisher, dict) and "_id" in publisher:
            publisher_id = publisher["_id"]
        else:
            print("Formato publisher non valido:", publisher)
            continue

        result = subprocess.run(
            [
                "curl", "-X", "PUT", f"http://localhost:8888/publishers/{publisher_id}",
                "-H", "Content-Type: application/json",
                "-d", json.dumps(publisher_update_data)
            ],
            capture_output=True, text=True
        )
        print(f"PUT /publishers/{publisher_id} result:")
        print(result.stdout)


# Funzione per eliminare un publisher
def test_delete_publisher():
    publishers = get_publishers_from_db()

    for publisher in publishers:
        if isinstance(publisher, dict) and "_id" in publisher:
            publisher_id = publisher["_id"]
        else:
            print("Formato publisher non valido:", publisher)
            continue

        result = subprocess.run(
            [
                "curl", "-X", "DELETE", f"http://localhost:8888/publishers/{publisher_id}",
            ],
            capture_output=True, text=True
        )
        print(f"DELETE /publishers/{publisher_id} result:")
        print(result.stdout)


# Funzione principale per eseguire tutti i test
def main():
    print("\n--- Running tests ---\n")

    test_create_publisher()
    test_create_books()
    test_update_book()
    test_delete_book()
    test_update_publisher()
    test_delete_publisher()


if __name__ == "__main__":
    main()
