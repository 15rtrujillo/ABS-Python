from typing import Callable


class Book:
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
        for property_name, value in kwargs.items():
            if self.custom_properties.get(property_name) is None:
                self.custom_properties[property_name] = value
                self._notify_property_changed("custom_properties")
                self._notify_property_changed(property_name)
            else:
                self.custom_properties[property_name] = value
                self._notify_property_changed(property_name)

    def remove_custom_property(self, key: str):
        try:
            del self.custom_properties[key]
        except KeyError as e:
            print(f"Attempting to delete property {key} from book {self.id}. Property does not exist.\n{repr(e)}")

    def _notify_property_changed(self, property_name: str):
        for observer in self.observers:
            observer(property_name)
