import os.path
from abc import abstractmethod

import pandas as pd

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
        """
        method to check the validity of a given facebook page name.

        Args:
            page_name ([string]): Facebook page name entered by the user

        Returns:
            boolean: represents the existance of given page name
        """
        exists, page = self.info(page_name)
        self.page_details = page
        return exists

    def fb_page_posts(self, page_name: str):
        """
        method to fetch facebook posts from the facebook scrapper
        
        Args:
            page_name (str): valid facebook page name
        
        Returns:
            returns: data length
        """
        file_path = "./data/%s/comments.csv" % page_name.lower()
        
        def get_length(file_path):
            with open(file_path, "r", encoding='UTF8') as file:
                content = [line.rstrip() for line in file]
                
                return len(content)

        if os.path.isfile("./data/%s/comments.csv" % page_name.lower()):
            return get_length(file_path)
        else:
            self.page_posts = self.posts(page_name)
            self.extract_comments()
            return get_length(file_path)

    def extract_comments(self):
        """ """
        try:
            comments = list()
            posts = list()
            for post in self.posts:
                for comment in post["comments_full"]:
                    comments.append(comment)
                    for reply in comment["replies"]:
                        comments.append(reply)

            self.save_posts(comments, posts)

        except Exception:
            pass
    
    def save_posts(self, comments, posts):
        import pandas as pd

        self.create_dir(self.page_name)
        df_posts = pd.DataFrame(posts)
        df_comments = pd.DataFrame(comments)

        df_posts.to_csv(
            "./data/%s/posts.csv" % self.page_name.lower(),
            sep=",",
            index=True,
            header=True,
        )
        df_comments.to_csv(
            "./data/%s/comments.txt" % self.page_name.lower(),
            sep=",",
            index=True,
            header=True,
        )

    
    def create_dir(self,page_name):
        """
        make a new directory for non-existing page data directory

        Args:
            page_name (str)

        Returns:
            [boolen]: return True if the directory not exist and make it 
                    return False if the directory exist 
        """
        import os

        dir_path = "./data/%s" % page_name.lower()
        if not os.path.isdir(dir_path):
            os.mkdir(dir_path)
            return True
        else:
            return False

  
    def commenters(self,page_name: str):
        try:
            df_comments = pd.read_csv("./data/%s/comments.csv" % page_name.lower())
            comments_desc = df_comments["commenter_name"].describe()
            top_commenter = "Name: {} - Comments: {}".format(
                comments_desc.top, comments_desc.freq
            )
            return top_commenter
        except Exception:
            print('No data Found')
        
