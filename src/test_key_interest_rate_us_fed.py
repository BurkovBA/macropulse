import unittest

import key_interest_rate_us_investing


class InlationKeyInterestRateUnitTest(unittest.TestCase):
    """python -m unittest test_module.TestClass.test_method"""
    def test_get_url(self):
        url = key_interest_rate_us_investing.get_url()
        print(url)

    def test_get_release_text(self):
        release_text = key_interest_rate_us_investing.get_release_text("https://www.federalreserve.gov/newsevents/pressreleases/monetary20230201a.htm")
        print(release_text)
