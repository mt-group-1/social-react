from fetch_posts.scrapper import Scraper
from socialreact.app import App


def welcome():
    import os

    os.system("cls" if os.name == "nt" else "clear")

    print("Welcome")
    print("Where you can analyize any facebook page posts")
    print("======================================================================")


if __name__ == "__main__":
    welcome()
    app_ = App(Scraper)
    app_.start()
    app_.user_menu_choice()
