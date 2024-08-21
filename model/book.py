class Book:
    def __init__(self, title: str, author: str, publication_year: str, custom_properties: list[str]):
        self.id = -1
        self.title = title
        self.author = author
        self.publication_year = publication_year
        self.custom_properties: dict[str, str] = {}
        for custom_property in custom_properties:
            self.custom_properties[custom_property] = ""

    def define_custom_property(self, **kwargs):
        for property in kwargs.keys():
            self.custom_properties[property] = kwargs[property]
