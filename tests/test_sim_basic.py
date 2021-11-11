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

def test_valid_page():
    app_ = App(Scraper)
    diffs = diff(app_, path="tests/sim/valid_fb_name.txt")
    assert not diffs, diffs
