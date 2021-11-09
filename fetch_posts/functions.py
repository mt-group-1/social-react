import warnings

warnings.filterwarnings("ignore")

import pandas as pd
from facebook_scraper import get_page_info, get_posts


def validate_page(page_name):
    """
    This function uses a dictonary that detect if the page name has a valid english name or not
    
    Args:
        page_name: String
    
    Returns:
        Boolean
    """
    page = get_page_info(page_name, options={"progress": True})
    if len(page) > 0:
        return True , page
    else:
        return False


def get_fb_posts(page_name):
    posts = get_posts(
        page_name,
        pages=2,
        options={"comments": True, "progress": True},
        cookies="./cookies/cookies.json",
    )
    return posts
