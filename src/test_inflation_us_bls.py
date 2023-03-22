import unittest

import inflation_us_bls


class InlationUsBlsUnitTest(unittest.TestCase):
    """python -m unittest test_module.TestClass.test_method"""
    def test_get_highcharts_plot(self):
        image = inflation_us_bls.get_highcharts_plot()
        image.save('tmp_image.png')

    def test_get_text(self):
        header, main_text = inflation_us_bls.get_text()
        print(header)
        print(main_text)
