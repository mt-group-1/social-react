import pytest
from fetch_posts.scrapper import Scraper
from socialreact.app import App

from tests.flo import diff

pytestmark = [pytest.mark.simulator]


def test_quit():
    app_ = App(Scraper)
    diffs = diff(app_, path="tests/sim/quit.sim.txt")
    assert not diffs, diffs

def test_invalid_input():
    app_ = App(Scraper)
    diffs = diff(app_, path="tests/sim/invalid_input.sim.txt")
    assert not diffs, diffs
    
def test_invalid_inputs():
    app_ = App(Scraper)
    diffs = diff(app_, path="tests/sim/invalid_input_2.txt")
    assert not diffs, diffs

def test_help_option():
    app_ = App(Scraper)
    diffs = diff(app_, path="tests/sim/help.txt")
    assert not diffs, diffs

def test_data_length():
    app_ = App(Scraper)
    diffs = diff(app_, path="tests/sim/data_length.txt")
    assert not diffs, diffs
    
def test_re_enter_page_name():
    app_ = App(Scraper)
    diffs = diff(app_, path="tests/sim/re_enter.txt")
    assert not diffs, diffs

def test_most_commenter():
    app_ = App(Scraper)
    diffs = diff(app_, path="tests/sim/commenter.txt")
    assert not diffs, diffs

def test_slow_model():
    app_ = App(Scraper)
    diffs = diff(app_, path="tests/sim/slow.txt")
    assert not diffs, diffs

def test_slow_model():
    app_ = App(Scraper)
    diffs = diff(app_, path="tests/sim/data_len_option.txt")
    assert not diffs, diffs

def test_predict_posts():
    app_ = App(Scraper)
    diffs = diff(app_, path="tests/sim/perdict_post.txt")
    assert not diffs, diffs
# @pytest.mark.skip("gh_code_action_reject_login")
# def test_valid_page():
#     app_ = App(Scraper)
#     diffs = diff(app_, path="tests/sim/valid_fb_name.txt")
#     assert not diffs, diffs