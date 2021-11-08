"""
    This module for testing social react program fuctions
"""
import pytest
from analyzer.data_processing import get_data
from analyzer.predictions import predict_post
from socialreact.main import check_page_info, check_post_words


def test_version():
    actual_version ='0.1.0'
    assert actual_version == '0.1.0'

def test_fb_page_name_exist():
    # Arrange 
    expected = True
    #Act 
    actual = check_page_info("Renad")
    #Assert
    assert actual == expected

def test_fb_page_name_not_exist():
    # Arrange 
    expected = False
    #Act 
    actual = check_page_info("Odeh")
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

@pytest.mark.skip("Todo")
def test_getting_data_after_scraping_sad_path():
    with pytest.raises(Exception):

        actual = get_data()

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
