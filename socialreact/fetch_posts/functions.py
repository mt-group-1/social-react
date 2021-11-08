import warnings

warnings.filterwarnings('ignore')

import pandas as pd
from facebook_scraper import get_page_info, get_posts


def validate_page(page_name):
    page = get_page_info(page_name)
    return True if len(page) > 0 else False

validate_page('Google')


def get_fb_posts(page_name):
    posts = get_posts(page_name, pages=5, options={"comments": True})
    return posts    
