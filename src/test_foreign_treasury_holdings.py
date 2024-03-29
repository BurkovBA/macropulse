import unittest

import foreign_treasury_holdings


class ForeignTreasuryHoldingsUnitTest(unittest.TestCase):
    """python -m unittest test_module.TestClass.test_method"""
    def test_get_pre_as_image(self):
        image = foreign_treasury_holdings.get_pre_as_image()
        image.save('tmp_image.png')
        # with open('tmp_image.png', 'wb') as file:
        #     file.write(image)

    def test_get_pre_as_dataframe(self):
        df = foreign_treasury_holdings.get_pre_as_dataframe()
        print(df)

    def test_get_plot(self):
        df = foreign_treasury_holdings.get_pre_as_dataframe()
        foreign_treasury_holdings.get_plot(df)

    def test_sort_holdings_by_abs_change(self):
        df = foreign_treasury_holdings.get_pre_as_dataframe()
        sorted_df = foreign_treasury_holdings.sort_holdings_by_abs_change(df)
