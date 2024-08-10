import json


class Booklist:
    def __init__(self, name: str, is_user_created: bool, books: list[int]):
        self.name = name
        self.books: list[int] = books
        self.is_user_created = is_user_created
