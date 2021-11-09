from random import randrange

from pyfiglet import Figlet
from termcolor import colored

from fetch_posts.scrapper import Scraper
from socialreact.app import App


def welcome():
    import os
    
    os.system("cls" if os.name == "nt" else "clear")
    
    logo = Figlet(font="slant")
    print(colored(logo.renderText("Social React"), "cyan"))
    print(colored(("Welcome social react"), "white"))
    print(colored(("Where you can analyize any facebook page posts"), "white"))
    print(colored(("=" * 70), "cyan"))


if __name__ == "__main__":
    welcome()
    app_ = App(Scraper)
    app_.start()
