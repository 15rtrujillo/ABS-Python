from model.book import Book
from model.booklist import Booklist
from typing import Final


import file_utils
import json


class Bookshelf:
    """Class for storing data used in the program"""

    BUILT_IN_PROPERTIES: Final[list[str]] = ["_title", "_author", "_publication_year"]
    BUILT_IN_PROPERTIES_DISPLAY: Final[list[str]] = ["Title", "Author", "Publication Year"]
    CUSTOM_PROPERTIES: list[str] = []

    def __init__(self):
        self.books: dict[int, Book] = {}
        self.booklists: dict[str, Booklist] = {}
        self.max_book_id: int = -1

    def _load_books(self):
        """Attempt to load the Bookshelf.abs file which contains information on all books."""
        # Read in the books
        try:
            bookshelf_file = open(file_utils.get_data_file_path("Bookshelf.abs"), "r")
        except FileNotFoundError:
            print("Bookshelf.abs file does not exist")
            print("File will be created upon first book creation")
            return
        
        try:
            bookshelf_json = json.loads(bookshelf_file.read())
        except json.JSONDecodeError as e:
            print("Error decoding Bookshelf JSON: " + repr(e))
            exit()
        
        for book in bookshelf_json:
            id = book["id"]
            if id > self.max_book_id:
                self.max_book_id = id

            # The following line creates a list from the dictionary keys
            custom_properties: list[str] = [*book["custom_properties"]]
            if not Bookshelf.CUSTOM_PROPERTIES:
                Bookshelf.CUSTOM_PROPERTIES = custom_properties
            elif Bookshelf.CUSTOM_PROPERTIES != custom_properties:
                print("Custom properties mismatch!")
                print("Current Properties:", Bookshelf.CUSTOM_PROPERTIES)
                print(f"Book ID {id} Properties: {str(custom_properties)}") 
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

    def _load_booklists(self):
        """Attempt to load all the .list files in the Data directory"""
        file_names = file_utils.get_files_in_directory(file_utils.get_data_directory())
        for file_name in file_names:
            if not ".list" in file_name:
                continue

            try:
                list_file = open(file_utils.get_data_file_path(file_name), "r")
            except FileNotFoundError:
                print("File not found for some reason:", file_name)
                continue

            try:
                list_json = json.loads(list_file.read())
            except json.JSONDecodeError as e:
                print(f"Couldn't parse JSON for booklist \"{file_name}\"\n{repr(e)}")
                continue

            books: list[Book] = []
            for book_id in list_json["books"]:
                books.append(self.books[book_id])

            new_booklist = Booklist(list_json["name"], True, books)
 
            self.booklists[list_json["name"]] = new_booklist

    def save_books(self):
        """Save all books to the Bookshelf.abs file"""
        file = open(file_utils.get_data_file_path("Bookshelf.abs"), "w")

        json.dump([*self.books.values()], file, default=vars, indent=4)

    def save_booklists(self):
        """Saves all the booklists to respective .list files"""
        for booklist in self.booklists.values():
            if not booklist.IS_USER_CREATED:
                continue

            file_name = booklist.name + ".list"
            file = open(file_utils.get_data_file_path(file_name), "w")
            
            json.dump(booklist, file, default=booklist.serialize, indent=4)

    def load(self):
        """Attempts to load books and booklists from the Data directory.
        If the Data directory does not exists (first run), one is created."""
        # Check if the data directory exists. If it doesn't, we create it
        if not file_utils.data_directory_exists():
            print("Data directory does not exist. Creating...")
            file_utils.create_data_directory()
        
        self._load_books()

        all_books = Booklist("All Books", False, [*self.books.values()])
        self.booklists[all_books.name] = all_books

        self._load_booklists()

    def save(self):
        """Save all data: books and booklists"""
        # Check if the data directory exists. If it doesn't, we create it
        if not file_utils.data_directory_exists():
            print("Data directory does not exist. Creating...")
            file_utils.create_data_directory()

        self.save_booklists()
        self.save_books()

    def backup(self):
        """Create a zip file of the current contents of the Data directory.
        Only keep a certain number of backups at a time."""
        # Data directory should always exist by now, since load is called first.
        backups_to_keep = 5

        # Check if Bookshelf.abs exists
        if not file_utils.os.path.exists(file_utils.get_data_file_path("Bookshelf.abs")):
            print("Bookshelf.abs does not exist. Unable to backup at this time")
            return
        
        files_in_directory = file_utils.get_files_in_directory(file_utils.get_data_directory())

        backup_files = [file for file in files_in_directory if ".backup" in file]

        if len(backup_files) >= backups_to_keep:
            # This should delete the oldest file
            file_utils.delete_file(file_utils.get_data_file_path(backup_files[0]))

        # Create a new backup
        file_utils.create_backup_file()

'''
    def add_book(self, book: Book, booklists: list[str] | None = None):
        """Create a new book, give it an ID, and add it to the specified booklists if any were given.
        Save the book to file."""
        self.max_book_id += 1
        book_id = self.max_book_id

        book.id = book_id

        self.books[book_id] = book
        self.booklists["All Books"].books.append(book)

        if booklists is not None:
            for booklist_name in booklists:
                self.booklists[booklist_name].books.append(book)

        self.save()

    def update_book(self, book: Book, include_in_booklists: list[str] = []):
        """Replaces a book with a newer version and saves it to file.
        Also adds it to the specified booklists and removes it from booklists not specified."""
        # Replace the book with the new one
        self.books[book.id] = book
        include_in_booklists.append("All Books")

        for booklist_name, booklist in self.booklists.items():
            # Remove the old book if it already exists in the booklist.
            booklist.remove_book_by_id(book.id)

            # If this is a list we want to add the book to, add it.
            if booklist_name in include_in_booklists:
                booklist.books.append(book)

        self.save()

    def delete_book(self, book: Book):
        """Deletes a book from memory, all booklists, and files"""
        for booklist in self.booklists.values():
            booklist.remove_book_by_id(book.id)
        
        del self.books[book.id]

        self.save()

    def new_booklist(self, name: str):
        """Create a new booklist and .list file if one of the same name does not already exist."""
        # Check if the new name already exists
        if name.casefold() in [n.casefold() for n in self.booklists.keys()]:
            raise ValueError()
        
        new_booklist = Booklist(name, True, [])
        self.booklists[name] = new_booklist

        self.save_booklists()

    def rename_booklist(self, old_name: str, new_name: str):
        """Rename a booklist and its file if one of the same name does not already exist"""
        # Check if the new name already exists
        if new_name.casefold() in [n.casefold() for n in self.booklists.keys()]:
            raise ValueError()
        
        booklist = self.booklists[old_name]

        del self.booklists[old_name]

        # Delete the file
        old_file_name = "Data/" + old_name + ".list"
        file_utils.delete_file(file_utils.get_file_path(old_file_name))

        booklist.name = new_name
        self.booklists[new_name] = booklist

        self.save_booklists()

    def delete_booklist(self, booklist: Booklist):
        """Delete a booklist from memory and disk"""
        # Delete the file
        old_file_name = "Data/" + booklist.name + ".list"
        file_utils.delete_file(file_utils.get_file_path(old_file_name))
        
        del self.booklists[booklist.name]
        
        self.save_booklists()

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
'''