import os.path

from fetch_posts.functions import get_fb_posts, validate_page


class Scraper:

    # region docstrings
    """
    This class will be responsible for fetching and preparing data for analysis.


    methods :

    page_info:
    --------
    check if the given page name is a valid and public facebook page

    args : page_name -> (string)

    returns : boolean : indicating if the page exists on facebook or not.



    page_posts:
    --------
    get facebook page posts and store them as class attribute.

    process comnents extraction.
    process data clean up.
    process save data to desk.

    args :  page_name ->  (string)

    returns : posts_length ->  (int) the length of page posts retrieved


    extract_comments:
    --------

     args : posts : (obj)

     returns comments : (list)


    clean_data:
    --------

    args : comments : (list)

    returns : comments : (list)


    save_data:
    --------

    args : None

    returns : boolean : indicating the success or failure of data save on desk

    """
    # endregion
    def __init__(self, info=validate_page, posts=get_fb_posts):
        self.info = info
        self.posts = posts
        self.page_name = None
        self.page_posts = None
        self.page_details = None

    def page_info(self, page_name):
        exists, page = self.info(page_name)
        self.page_details = page
        return exists

    def fb_page_posts(self, page_name: str):
        file_path = "./data/%s_comments.txt" % page_name.lower()

        def get_length(file_path):
            with open(file_path, "r", encoding='UTF8') as file:
                content = [line.rstrip() for line in file]

                return len(content)

        if os.path.isfile(file_path):
            return get_length(file_path)
        else:
            self.page_posts = self.posts(page_name)
            self.extract_comments()
            return get_length(file_path)

    def extract_comments(self):
        list_of_posts = list()
        list_of_comments = list()

        for post in self.page_posts:
            list_of_posts.append(
                {
                    "post_id": post["post_id"],
                    "time_stamp": post["timestamp"],
                    "text": post["text"],
                    "likes": post["likes"],
                    "comments": post["comments"],
                    "comments_full": post["comments_full"],
                }
            )

            for comment in list_of_posts[-1]["comments_full"]:
                list_of_comments.append(comment["comment_text"])

        self.save_posts(list_of_comments, list_of_posts)

    def save_posts(self, comments, posts):
        import pandas as pd

        df_posts = pd.DataFrame(posts)
        df_comments = pd.DataFrame(comments)
        df_posts.to_csv(
            "./data/%s_posts.csv" % self.page_name.lower(),
            header=True,
            index=False,
        )
        df_comments.to_csv(
            "./data/%s_comments.txt" % self.page_name.lower(),
            sep=" ",
            index=True,
            header=False,
        )
