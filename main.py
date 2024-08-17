import bookshelf
import gui.abs as abs


def main():
    shelf = bookshelf.Bookshelf()
    shelf.load()

    window = abs.ABS(shelf)
    window.show_window()


if __name__ == "__main__":
    main()
