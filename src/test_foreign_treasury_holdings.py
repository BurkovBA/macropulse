import unittest

import foreign_treasury_holdings


class ForeignTreasuryHoldingsUnitTest(unittest.TestCase):
    """python -m unittest test_module.TestClass.test_method"""
    def test_get_pre_as_image(self):
        image = foreign_treasury_holdings.get_pre_as_image()
        with open('tmp_image.png', 'wb') as file:
            file.write(image)

    def test_get_pre_as_dataframe(self):
        df = foreign_treasury_holdings.get_pre_as_dataframe()
        print(df)
