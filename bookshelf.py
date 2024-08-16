from book import Book
from booklist import Booklist


import copy
import file_utils
import json


class Bookshelf:
    """Class for storing data used in the program"""
    def __init__(self):
        self.books: dict[int, Book] = {}
        self.booklists: dict[str, Booklist] = {}
        self.max_book_id: int = -1
        self.built_in_properties: list[str] = ["Title", "Author", "Publication Year"]
        self.custom_properties: list[str] = []

    def __load_books(self):
        """Attempt to load the Bookshelf.abs file which contains information on all books."""
        # Read in the books
        try:
            bookshelf_file = open(file_utils.get_file_path("Data/Bookshelf.abs"), "r")
        except FileNotFoundError:
            print("Bookshelf.abs file does not exist")
            return
        
        try:
            bookshelf_json = json.loads(bookshelf_file.read())
        except json.JSONDecodeError:
            print("Error decoding Bookshelf JSON")
            return
        
        for book in bookshelf_json:
            id = book["id"]
            if id > self.max_book_id:
                self.max_book_id = id

            # The following line creates a list from the dictionary keys
            custom_properties = [*book["custom_properties"]]
            if not self.custom_properties:
                self.custom_properties = custom_properties
            elif self.custom_properties != custom_properties:
                print("Custom properties mismatch!")
                exit()

            new_book = Book(
                book["title"],
                book["author"],
                book["publication_year"],
                custom_properties
            )
            new_book.id = id
            # The following line passes in the dictionary/JSON object as kwargs
            new_book.define_custom_property(**book["custom_properties"])

            self.books[id] = new_book

    def __load_booklists(self):
        """Attempt to load all the .list files in the Data directory"""
        file_names = file_utils.get_files_in_directory(file_utils.get_data_directory())
        for file_name in file_names:
            if file_name[file_name.find(".")+1:] != "list":
                continue

            try:
                list_file = open(file_utils.get_file_path("Data/" + file_name), "r")
            except FileNotFoundError:
                print("File not found for some reason:", file_name)
                continue

            try:
                list_json = json.loads(list_file.read())
            except json.JSONDecodeError:
                print("Couldn't parse JSON for booklist", file_name)
                continue

            new_booklist = Booklist(list_json["name"], True, list_json["books"])
 
            self.booklists[list_json["name"]] = new_booklist

    def __save_books(self):
        """Save all books to the Bookshelf.abs file"""
        file_name = "Data/Bookshelf.abs"
        file = open(file_utils.get_file_path(file_name), "w")

        json.dump([*self.books.values()], file, default=vars, indent=4)

    def __save_booklists(self):
        """Saves all the booklists to respective .list files"""
        for booklist in self.booklists.values():
            if not booklist.is_user_created:
                continue

            file_name = booklist.name + ".list"
            file = open(file_utils.get_file_path("Data/" + file_name), "w")
            
            json.dump(booklist, file, default=vars, indent=4)

    def load(self):
        """Attempts to load books and booklists from the Data directory.
        If the Data directory does not exists (first run), one is created."""
        # Check if the data directory exists. If it doesn't, we create it
        if not file_utils.data_directory_exists():
            print("Data directory does not exist. Creating...")
            file_utils.create_data_directory()
        
        self.__load_books()

        all_books = Booklist("All Books", False, [*self.books.keys()])
        self.booklists[all_books.name] = all_books

        self.__load_booklists()

    def save(self):
        """Save all data: books and booklists"""
        # Check if the data directory exists. If it doesn't, we create it
        if not file_utils.data_directory_exists():
            print("Data directory does not exist. Creating...")
            file_utils.create_data_directory()

        self.__save_booklists()
        self.__save_books()

    def get_books_from_booklist(self, booklist: Booklist | None = None, booklist_name: str | None = None) -> list[Book]:
        if booklist is None and booklist_name is None:
            raise TypeError("booklist and booklist_name cannot both be None")
        elif booklist is None:
            booklist = self.booklists[booklist_name]
            
        return [self.books[b_id] for b_id in booklist.books]

    def add_book(self, book: Book, booklists: list[str] | None = None):
        """Create a new book, give it an ID, and add it to the specified booklists if any were given.
        Save the book to file."""
        self.max_book_id += 1
        book_id = self.max_book_id

        book.id = book_id

        self.books[book_id] = book
        self.booklists["All Books"].books.append(book_id)

        if booklists is not None:
            for booklist_name in booklists:
                self.booklists[booklist_name].books.append(book_id)

        self.save()

    def update_book(self, book: Book, booklists: list[str] | None = None):
        """Replaces a book with a newer version and saves it to file.
        Also adds it to the specified booklists and removes it from booklists not specified."""
        # Replace the book with the new one
        self.books[book.id] = book

        for name, list in self.booklists.items():
            if not list.is_user_created:
                continue

            # If the current booklist is one the book should be in
            if name in booklists:
                # Check if it's in there. If it isn't, add it.
                if not book.id in list.books:
                    list.books.append(book.id)
            else:
                # If it shouldn't be in the booklist, remove it if it's there.
                if book.id in list.books:
                    list.books.remove(book.id)

        self.save()

    def delete_book(self, book: Book):
        """Deletes a book from memory, all booklists, and files"""
        for booklist in self.booklists.values():
            try:
                booklist.books.remove(book.id)
            except ValueError:
                continue
        
        del self.books[book.id]

        self.save()

    def new_booklist(self, name: str):
        """Create a new booklist and .list file if one of the same name does not already exist."""
        # Check if the new name already exists
        if name.casefold() in [n.casefold() for n in self.booklists.keys()]:
            raise ValueError()
        
        new_booklist = Booklist(name, True, [])
        self.booklists[name] = new_booklist

        self.__save_booklists()

    def rename_booklist(self, old_name: str, new_name: str):
        """Rename a booklist and its file if one of the same name does not already exist"""
        # Check if the new name already exists
        if new_name.casefold() in [n.casefold() for n in self.booklists.keys()]:
            raise ValueError()
        
        old_booklist = self.booklists[old_name]
        new_booklist = copy.deepcopy(old_booklist)
        new_booklist.name = new_name

        del self.booklists[old_name]

        # Delete the file
        old_file_name = "Data/" + old_name + ".list"
        file_utils.delete_file(file_utils.get_file_path(old_file_name))

        self.booklists[new_name] = new_booklist

        self.__save_booklists()

    def delete_booklist(self, booklist: Booklist):
        """Delete a booklist from memory and disk"""
        # Delete the file
        old_file_name = "Data/" + booklist.name + ".list"
        file_utils.delete_file(file_utils.get_file_path(old_file_name))
        
        del self.booklists[booklist.name]
        
        self.__save_booklists()

    def new_property(self, name: str, default: str):
        """Add a new property to all books.
        The property should have already been checked to see if it's a duplicate."""
        self.custom_properties.append(name)

        for book in self.books.values():
            book.custom_properties[name] = default

        self.__save_books()

    def delete_property(self, name: str):
        """Deletes a property from all books"""
        self.custom_properties.remove(name)

        for book in self.books.values():
            del book.custom_properties[name]

        self.__save_books()
