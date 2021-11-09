import pandas as pd
from analyzer.com_classfiction import classify_comments
from termcolor import colored


class App:
    def __init__(self, scraper):
        """
        docs
        """
        self.user_name = None
        self.user_input = None
        self.page_name = None
        self.scraper = scraper()

    def start(self):
        print(
            colored(
                (
                    "Start page analysis (s) , Post impact prediction (i) , Help (h) , Quit(q) "
                ),
                "white",
            )
        )
        self.user_menu_choice()

    def user_menu_choice(self):
        def quit():
            print(
                colored(
                    ("thank you for using our application... see you later 👋"),
                    "cyan",
                )
            )
            exit()

        self.choice = input(" > ").lower()

        if self.choice == "q":
            quit()

        if self.choice == "s":

            def most_commenter():
                """
                sub method that get the most commenter user on a given page.
                """
                # TODO []: request posts and get comments .
                # TODO []: return the top 3 most commenters
                pass

            def valid_page():
                self.page_name = input("Enter FaceBook Page Name :  > ")
                return self.scraper.page_info(self.page_name)

            def confirm_page():
                print(
                    colored(
                        ("Found this page  ✔️ "),
                        "cyan",
                    ),
                    self.page_name,
                )
                page_info = ""
                page = self.scraper.page_details
                for key in page:
                    page_info += "{} : {} ".format(str(key), page[key])
                print(page_info, "\n")
                choice = input(
                    "Press (Enter) to continue , (s) to re-enter page name > "
                ).lower()

                if choice == "s":
                    valid_page()
                else:
                    return True

            if not valid_page():
                print(
                    colored(
                        ("invalid page name..  ❌ "),
                        "cyan",
                    ),
                    self.page_name,
                )

                self.choice = input(
                    "Press (Enter) to continue , (q) to Quit  > "
                ).lower()

                if self.choice == "q":
                    quit()

                else:
                    valid_page()

            if confirm_page():
                # ! validate fetched posts length
                length = self.scraper.fb_page_posts(self.page_name)

                if length < 200:
                    print("The page entered do not have enogh content")
                    print("Which will lead to inaccurate prediction results..")
                    print("-" * 80)
                    print("But we can give you the most common commenter")
                    choice = input("to do that , press ( ENTER ) (q) to quit > ")

                    if choice == "q":
                        quit()

                    most_commenter()

                if length > 200:
                    print("Starting comments classification ...")
                    comments = classify_comments(
                        "./data/%s_comments.txt" % self.page_name.lower(),
                        self.page_name.lower(),
                    )
                    print(comments.head(20))
                    # TODO []: send the DataFrame to processing .
                    # TODO []: finalize the comments analysis feature.

        if self.choice == "i":
            pass

        if self.choice == "h":
            pass

    def check_post_words(self, post):
        """
        This function is resposiable for checking the post given if its an english valid or invalid

        Args:
            post_: String

        Returns:
            Boolean,True if the page name is valid, False if the post is invalid
        """
        pass

    def check_page_info(self):

        """
        This function uses a dictonary that detect if the page name has a valid english name or not

        Args:
            page_name: String

        Returns:
            Boolean
        """
        pass
