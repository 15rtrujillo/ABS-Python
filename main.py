import bookshelf
import gui.abs as abs


def main():
    shelf = bookshelf.Bookshelf()
    shelf.load()
    shelf.backup()

    window = abs.ABS(shelf)
    window.show_window()


if __name__ == "__main__":
    main()
