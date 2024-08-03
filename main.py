import gui.abs as abs
import bookshelf


def main():
    shelf = bookshelf.Bookshelf()
    shelf.load()

    window = abs.ABS(shelf)
    window.show_window()


if __name__ == "__main__":
    main()
