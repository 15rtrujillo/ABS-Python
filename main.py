from bookshelf import Bookshelf


import abs


def main():
    bookshelf = Bookshelf()
    bookshelf.load()

    window = abs.ABS(bookshelf)
    window.show_window()


if __name__ == "__main__":
    main()
