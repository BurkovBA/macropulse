import unittest

import key_interest_rate_ru_cbrf


class InlationKeyInterestRateUnitTest(unittest.TestCase):
    """python -m unittest test_module.TestClass.test_method"""
    def test_get_plot(self):
        image = key_interest_rate_ru_cbrf.get_plot()
        image.save('tmp_image.png')

    def test_get_text(self):
        key_interest_rate = key_interest_rate_ru_cbrf.get_key_interest_rate()
        print(key_interest_rate)
