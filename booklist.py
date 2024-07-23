import book as b


class Booklist:
    def __init__(self, name: str, *books: b.Book):
        self.name = name
        self.books: list[b.Book] = []
        for book in books:
            self.books.append(book)