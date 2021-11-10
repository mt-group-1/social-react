"""
    This module for testing social react program fuctions
"""
import io
import warnings
import pytest
import socialreact
from unittest import mock
from unittest.mock import patch
from analyzer.com_classfiction import classify_comments
from analyzer.predictions import predict_post
from fetch_posts.functions import get_fb_posts, validate_page
from fetch_posts.scrapper import Scraper
from socialreact import *
from socialreact import __version__
from io import StringIO
from analyzer.data_processing import ModelCreator
import fetch_posts.scrapper as scraper
from socialreact.app import App
warnings.filterwarnings("ignore")
from main import welcome


def test_version():
    assert __version__ == "0.1.0"

@pytest.mark.skip("gh_code_action_reject_login")
def test_fb_page_name_exist():
    # Arrange
    expected = True
    # Act
    exists, _ = validate_page("Google")
    actual = exists
    # Assert
    assert actual == expected

@pytest.mark.skip("gh_code_action_reject_login")
def test_fb_page_name_not_exist():
    # Arrange
    expected = False
    # Act
    exists, _ = validate_page("Odeh")
    actual = exists
    # Assert
    assert actual == expected

@pytest.mark.skip("pending")
def test_positive_prediction():
    # Arrange
    expected = "Recommended"
    post = "This text for testing"
    # Act
    actual = predict_post(post)
    # Assert
    assert actual == expected

@pytest.mark.skip("pending")
def test_negative_prediction():
    # Arrange
    expected = "Recommended"
    post = "This text for testing"
    # Act
    actual = predict_post(post)
    # Assert
    assert actual == expected

def test_page_content():
    # Arrange
    expected = "<class 'generator'>"
    # Act
    actual = str(type(get_fb_posts("Google")))
    # Assert
    assert actual == expected

def test_scrape_page_post():
    # Arrange
    expected = True
    # Act
    page_scraper = Scraper()
    actual = page_scraper.page_info("Google")
    # Assert
    assert actual == expected

@pytest.mark.skip()  # file i/o operation
def test_scrape_page_post_length():
    # Arrange
    page_scraper = Scraper()
    expected = ""
    # Act
    actual = page_scraper.fb_page_posts("Google")
    # Assert
    assert actual == expected

def test_labeling_file_positive_case():
    # Arrange
    expected = 1
    # Act
    actual = classify_comments("./data/test_/positive.txt", "test").values.tolist()[0][
        1
    ]

    # Assert
    assert actual == expected

def test_labeling_file_negative_case():
    # Arrange
    expected = 0
    # Act
    actual = classify_comments("./data/test_/negative.txt", "test").values.tolist()[0][
        1
    ]
    # Assert
    assert actual == expected

def test_labeling_file_nutral_case():
    # Arrange
    expected = "N"
    # Act
    actual = classify_comments("./data/test_/nutral.txt", "test").values.tolist()[0][1]
    # Assert
    assert actual == expected

app_ = App(Scraper)

@patch("sys.stdout", fake_out=io.StringIO())
def test_welcome_msg(mock_stdout):
    file = open("./test_stdout/test_welcome_message.txt", "r")
    text = file.readlines()
    # Arrange
    with patch("sys.stdout", new=StringIO()) as fake_out:
        # Act
        welcome()
        stdout = fake_out.getvalue()
        stdout = stdout.split("\n")
        for idx, expected in enumerate(text):
            # Assert
            assert stdout[idx].replace("\n", "") == expected.replace("\n", "")

@patch("sys.stdout", new_callable=io.StringIO)
def test_start_msg(mock_stdout):
    # Arrange
    expected = "\x1b[37mStart page analysis (s) , Post impact prediction (i) , Help (h) , Quit(q)\x1b[0m\n"
    # Act
    app_.start()
    actual = mock_stdout.getvalue().encode("utf8", "backslashreplace").decode("utf8")

    # Assert
    assert actual == expected

def test_quit_msg(monkeypatch):
    # Arrange
    expected = "thank you for using our application... see you later 👋"
    mock_input = StringIO("q\n")
    monkeypatch.setattr("sys.stdin", mock_input)
    try:
        assert app_.user_menu_choice() == expected
    except SystemExit:
        pass

def test_most_common_commenter():
    #Arrange 
    expected = "Name: Nancy Henry - Comments: 14"
    # Act 
    s = Scraper()
    actual = s.commenters("Google")
    #Assert
    assert actual == expected

@pytest.mark.skip()
def test_create_directury():
    #Arrange 
    expected = True
    # Act 
    s = Scraper()
    actual = s.commenters("Google")
    #Assert
    assert actual == expected

model = ModelCreator("cnn")
model.page_comments()

def test_page_have_comment():

   assert model.keras() == True

def test_page_comment_impact():
    #Arrange
    expected = "This page has POSITIVE impact on its followers"
    # Act 
    actual =  model.page_comments()
    #Assert
    assert actual == expected

def test_train_model_score_and_accuracy():
    #Arrange
    expected = ("score    --> 0.52 accuracy -->  0.73")
    # Act 
    score,acu = model.train_model()
    actual = (score ,acu)
    #Assert
    assert actual == expected
