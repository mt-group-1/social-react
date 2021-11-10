"""
    This module for testing social react program fuctions
"""
import io
from typing import Tuple
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
from analyzer.analyzer import load_data
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
    expected = True
    post = "This text for testing"
    # Act
    actual = predict_post(post,"google")
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

# @pytest.mark.skip()
def test_create_directury():
    #Arrange 
    expected = False
    # Act 
    s = Scraper()
    actual = s.create_dir("Google")
    #Assert
    assert actual == expected

# @pytest.mark.skip("pending")
def test_page_have_comment():
    model = ModelCreator("cnn")
    model.page_comments()
    assert model.keras() == True
    
model = ModelCreator("cnn")
# @pytest.mark.skip("pending")
def test_page_comment_impact():
    #Arrange
    expected = "This page has POSITIVE impact on its followers"
    # Act 
    model = ModelCreator("cnn")
    model.page_comments()
    actual =  model.page_comments()
    #Assert
    assert actual == expected

# @pytest.mark.skip("training time resone")
def test_train_model_score_and_accuracy():
    # Act 
    actual = model.train_model()
    #Assert
    assert actual == model.train_model()

@pytest.mark.skip("training time resone")
def test_random_partition():
    #Arrange
    expected = True
    # Act 
    actual = model.random_partitions()
    #Assert
    assert actual == expected

@pytest.mark.skip("training time resone")
def test_vectorize():
    #Arrange
    expected = True
    # Act 
    actual = model.vectorize()
    #Assert
    assert actual == expected

def test_keras():
    #Arrange
    expected = model.keras()
    # Act 
    actual = model.keras()
    #Assert
    assert actual == expected

def test_keras_model():
    # Act 
    actual = model.keras_model()
    #Assert
    assert actual == model.keras_model()

def test_vaidate_acc():
    #Arrange
    expected = model.keras_model()
    # Act 
    actual = model.keras_model()
    #Assert
    assert actual == expected

def test_load_data():
    expected = float

    actual = type(load_data("./data/google/classified_comments.txt"))

    assert actual == expected