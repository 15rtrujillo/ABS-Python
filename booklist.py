from book import Book


class Booklist:
    def __init__(self, name: str, is_user_created: bool, books: list[Book]):
        self.name = name
        self.books = books
        self.is_user_created = is_user_created

    def get_book_by_id(self, id: int) -> Book | None:
        for book in self.books:
            if id == book.id:
                return book
        return None
    
    def remove_book_by_id(self, id: int):
        for book in self.books:
            if id == book.id:
                self.books.remove(book)

    def get_book_ids(self) -> list[int]:
        ids: list[int] = []
        for book in self.books:
            ids.append(book.id)
        return ids

    @staticmethod
    def serialize(obj) -> dict[str]:
        if isinstance(obj, Booklist):
            serialized = {"name": obj.name,
                          "books": [book.id for book in obj.books],
                          "is_user_created": obj.is_user_created}
            return serialized
        else:
            raise TypeError(f"Unserializable object {obj} of type {type(obj)}")
