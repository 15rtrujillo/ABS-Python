import abs


from bookshelf import Bookshelf


def main():
    bookshelf = Bookshelf()
    bookshelf.load()
    window = abs.ABS(bookshelf)


if __name__ == "__main__":
    main()
