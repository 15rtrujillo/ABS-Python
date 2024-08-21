from model.book import Book
from typing import Callable, Final


class Booklist:
    def __init__(self, name: str, is_user_created: bool, books: list[Book]):
        self._name = name
        self._books = books
        self.IS_USER_CREATED: Final[bool] = is_user_created
        self.observers: list[Callable[[str], None]] = []

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value
        self._notify_property_changed("name")

    def add_book(self, book: Book):
        self._books.append(book)
        self._notify_property_changed("books")

    def remove_book_by_id(self, id: int):
        for book in self._books:
            if id == book.id:
                self._books.remove(book)
                self._notify_property_changed("books")

    def get_book_by_id(self, id: int) -> Book | None:
        for book in self._books:
            if id == book.id:
                return book
        return None
    
    def has_book(self, id: int) -> bool:
        for book in self._books:
            if id == book.id:
                return True
        return False

    def get_book_ids(self) -> list[int]:
        ids: list[int] = []
        for book in self._books:
            ids.append(book.id)
        return ids

    def _notify_property_changed(self, property_name):
        for observer in self.observers:
            observer(property_name)

    @staticmethod
    def serialize(obj) -> dict[str]:
        if isinstance(obj, Booklist):
            serialized = {"name": obj.name,
                          "books": [book.id for book in obj.books],
                          "is_user_created": obj.is_user_created}
            return serialized
        else:
            raise TypeError(f"Unserializable object {obj} of type {type(obj)}")
