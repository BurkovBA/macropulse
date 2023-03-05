import unittest

import inflation_ru_rosstat


class InlationRuRosstatUnitTest(unittest.TestCase):
    """python -m unittest test_module.TestClass.test_method"""
    def test_get_url(self):
        current_date = '01-03-2023'
        url = inflation_ru_rosstat.get_url(current_date)
        self.assertEquals(url, 'https://rosstat.gov.ru/storage/mediabank/32_01-03-2023.html')

    def test_get_image(self):
        image = inflation_ru_rosstat.get_image()

        # Save the screenshot to a file
        with open("/tmp/element_screenshot.png", "wb") as f:
            f.write(image)
