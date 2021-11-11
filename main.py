
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
from pyfiglet import Figlet
from termcolor import colored

from fetch_posts.scrapper import Scraper
from socialreact.app import App


def welcome():
    print("Welcome")
    print("Where you can analyize any facebook page posts")
    print("======================================================================")

if __name__ == "__main__":
    welcome()
    app_ = App(Scraper)
    app_.start()
    app_.user_menu_choice()
