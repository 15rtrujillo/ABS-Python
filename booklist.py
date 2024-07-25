import json


class Booklist:
    def __init__(self, name: str, is_user_created: bool, *books: int):
        self.name = name
        self.books: list[int] = []
        for book in books:
            self.books.append(book)
        self.is_user_created = is_user_created


if __name__ == "__main__":
    test_booklist = Booklist("Wishlist", 0, 1)
    
    test_file = open(test_booklist.name + ".list", "w")
    test_file.write(json.dumps(test_booklist, default=vars))
