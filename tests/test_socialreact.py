"""
    This module for testing social react program fuctions
"""
import pytest
from socialreact import __version__
from fetch_posts.functions import validate_page, get_fb_posts
from analyzer.data_processing import get_data
from analyzer.predictions import predict_post
from socialreact.analyzer.com_classfiction import labeling
from fetch_posts.functions import validate_page
from socialreact.main import check_post_words
from fetch_posts.scrapper import Scraper
import warnings

warnings.filterwarnings('ignore')

def test_version():
    assert __version__ == '0.1.0'

@pytest.mark.skip()   # code action Login requerment
def test_fb_page_name_exist():
    # Arrange 
    expected = True
    #Act 
    actual = validate_page("Google")
    #Assert
    assert actual == expected

def test_fb_page_name_not_exist():
    # Arrange 
    expected = False
    #Act 
    actual = validate_page("Odeh")
    #Assert
    assert actual == expected

def test_getting_data_after_scraping_happy_path():
    #Arrange 
    expected = {
        "post_id":'12345',
        "post_txt": 'katha katha katha',
        "likes": 200
        }
    #Act
    actual = get_data("page_name")
    #Assert
    assert actual == expected

def test_positive_prediction():
    #Arrange 
    expected = 'Recommended'
    post = "This text for testing"
    #Act
    actual = predict_post(post)
    #Assert
    assert actual == expected

def test_negative_prediction():
    #Arrange 
    expected ='Recommended'
    post = "This text for testing"
    #Act
    actual = predict_post(post)
    #Assert
    assert actual == expected

def test_post_have_valid_words():
     #Arrange 
    expected =True
    post = "This text for testing"
    #Act
    actual = check_post_words(post)
    #Assert
    assert actual == expected

def test_post_have_invalid_words():
     #Arrange 
    expected =False
    post = "asdfg asdfgh sdfgh dfgh"
    #Act
    actual = check_post_words(post)
    #Assert
    assert actual == expected

@pytest.mark.skip()  # code action Login requerment
def test_enter_valid_page_name():
    # Arrange 
    expected = True
    #Act 
    actual = validate_page("Google")
    #Assert
    assert actual == expected

def test_enter_invalid_page_name():
    # Arrange 
    expected = False
    #Act 
    actual = validate_page("sdfg")
    #Assert
    assert actual == expected
    
def test_page_content():
    # Arrange 
    expected = "<class 'generator'>"
    #Act 
    actual = str(type(get_fb_posts("Google")))
    #Assert
    assert actual == expected

def test_scrape_page_post():
    # Arrange 
    expected = True
    #Act 
    page_scraper = Scraper("Google")
    actual = page_scraper.page_info()
    #Assert
    assert actual == expected

@pytest.mark.skip()  #file i/o operation 
def test_scrape_page_post():
    # Arrange 
    page_scraper = Scraper("Google")
    expected ="./data/Google_posts.csv"
    #Act 
    page_scraper.fb_page_posts()
    actual = page_scraper.page_posts
    #Assert
    assert actual == expected

# @pytest.mark.skip() 
def test_labeling_file_positive_case():
    # Arrange 
    expected = 1
    #Act 
    actual = labeling("./data/test_/positive")[0][1]
    #Assert
    assert actual == expected

def test_labeling_file_negative_case():
    # Arrange 
    expected = 0
    #Act 
    actual = labeling("./data/test_/negative")[0][1]
    #Assert
    assert actual == expected

def test_labeling_file_nutral_case():
    # Arrange 
    expected = "N"
    #Act 
    actual = labeling("./data/test_/nutral")[0][1]
    #Assert
    assert actual == expected