import unittest

import money_supply_ru_cbrf


class MoneySupplyRuCbrfUnitTest(unittest.TestCase):
    """python -m unittest test_module.TestClass.test_method"""
    def test_get_highcharts_plot(self):
        image = money_supply_ru_cbrf.get_image()
        image.save('tmp_image.png')

    def test_get_text(self):
        key_interest_rate = money_supply_ru_cbrf.get_money_supply()
        print(key_interest_rate)
