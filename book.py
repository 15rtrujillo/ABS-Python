import json


class Book:
    def __init__(self, id: int, title: str, author: str, publication_year: int, *custom_properties: str):
        self.id = id
        self.title = title
        self.author = author
        self.publication_year = publication_year
        self.custom_properties: dict[str, str] = {}
        for custom_property in custom_properties:
            self.custom_properties[custom_property] = ""

    def define_custom_property(self, **kwargs):
        for property in kwargs.keys():
            self.custom_properties[property] = kwargs[property]


if __name__ == "__main__":
    test_book = Book(0, "Aurora, My Love", "Ryan", 2024, *["Price", "Location"])
    test_book.define_custom_property(Price="$2.50", Location="Denmark")
    test_book2 = Book(1, "All About Aurora", "Someone Else", 1991, "Price", "Location")
    books = [test_book, test_book2]

    test_file = open("Bookshelf.abs", "w")
    test_file.write(json.dumps(books, default=vars))
