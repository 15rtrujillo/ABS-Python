from typing import Callable, Final


class Book:
    BUILT_IN_PROPERTIES: Final[list[str]] = ["_title", "_author", "_publication_year"]
    BUILT_IN_PROPERTIES_DISPLAY: Final[list[str]] = ["Title", "Author", "Publication Year"]

    def __init__(self, title: str, author: str, publication_year: str, custom_properties: list[str]):
        self.id = -1
        self._title = title
        self._author = author
        self._publication_year = publication_year
        self.custom_properties: dict[str, str] = {}
        for custom_property in custom_properties:
            self.custom_properties[custom_property] = ""
        self.observers: list[Callable[[str], None]] = []

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value: str):
        self._title = value
        self._notify_property_changed("Title")

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, value: str):
        self._author = value
        self._notify_property_changed("Author")

    @property
    def publication_year(self):
        return self._publication_year

    @publication_year.setter
    def publication_year(self, value: str):
        self._publication_year = value
        self._notify_property_changed("Publication Year")

    def define_custom_property(self, **kwargs: str):
        for property, value in kwargs.items():
            self.custom_properties[property] = value
            self._notify_property_changed(property)

    def remove_custom_property(self, key: str):
        try:
            del self.custom_properties[key]
        except KeyError as e:
            print(f"Attempting to delete property {key} from book {self.id}. Property does not exist.\n{repr(e)}")

    def _notify_property_changed(self, property_name: str):
        for observer in self.observers:
            observer(property_name)
