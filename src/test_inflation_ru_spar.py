import unittest
from io import BytesIO

import pandas as pd

import inflation_ru_spar


class InlationRuSparUnitTest(unittest.TestCase):
    """python -m unittest test_module.TestClass.test_method"""
    def test_get_current_prices(self):
        prices = inflation_ru_spar.get_current_prices()
        print(prices)

    def test_get_table_image(self):
        prices = {
            'Лук репчатый': 69.9,
            'Капуста белокачанная': 16.9,
            'Яблоки сезонные': 89.9,
            'Свекла красная': 29.9,
            'Курица филе': 319.9,
            'Молоко Простоквашино, 3.2%': 89.9,
            'Масло сливочное': 79.9,
            'Перец микс': 299.9,
            'Огурцы короткоплодные': 249.9,
            'Груша': 249.9,
            'Картофель': 25.9,
            'Киви': 149.9,
            'Огурцы тепличные среднеплодные': 259.9,
            'Морковь': 36.9,
            'Капуста цветная': 269.9,
            'Баклажаны с овощами': 129.9,
            'Кабачки': 199.9,
            'Песок сахарный 1 кг': 57.9,
            'Крупа гречневая 900г': 109.9
        }

        df = pd.DataFrame.from_dict(prices, orient='index')
        image_buffer = inflation_ru_spar.get_table_image(df)

        # Save the screenshot to a file
        with open("image.png", "wb") as f:
            f.write(image_buffer.getvalue())

    def test_get_inflation(self):
        prices = {
            'Лук репчатый': 69.9,
            'Капуста белокачанная': 16.9,
            'Яблоки сезонные': 89.9,
            'Свекла красная': 29.9,
            'Курица филе': 319.9,
            'Молоко Простоквашино, 3.2%': 89.9,
            'Масло сливочное': 79.9,
            'Перец микс': 299.9,
            'Огурцы короткоплодные': 249.9,
            'Груша': 249.9,
            'Картофель': 25.9,
            'Киви': 149.9,
            'Огурцы тепличные среднеплодные': 259.9,
            'Морковь': 36.9,
            'Капуста цветная': 269.9,
            'Баклажаны с овощами': 129.9,
            'Кабачки': 199.9,
            'Песок сахарный 1 кг': 57.9,
            'Крупа гречневая 900г': 109.9
        }
        previous_prices = prices
        inflation = inflation_ru_spar.get_inflation(prices, previous_prices)
        print(inflation)
