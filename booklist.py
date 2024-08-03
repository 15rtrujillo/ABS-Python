import json


class Booklist:
    def __init__(self, name: str, is_user_created: bool, *books: int):
        self.name = name
        self.books: list[int] = []
        for book in books:
            self.books.append(book)
        self.is_user_created = is_user_created
