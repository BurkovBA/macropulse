import unittest

import inflation_ru_rosstat


class InlationRuRosstatUnitTest(unittest.TestCase):
    """python -m unittest test_module.TestClass.test_method"""
    def test_get_page_url(self):
        url = inflation_ru_rosstat.get_page_url()
        self.assertEquals(url, 'https://rosstat.gov.ru/storage/mediabank/32_01-03-2023.html')

    def test_get_image(self):
        url = inflation_ru_rosstat.get_page_url()
        image = inflation_ru_rosstat.get_image(url)

        # Save the screenshot to a file
        with open("/tmp/element_screenshot.png", "wb") as f:
            f.write(image)

    def test_get_table(self):
        url = inflation_ru_rosstat.get_page_url()
        table = inflation_ru_rosstat.get_table(url)
        print(table.columns)
        print(table)

    def test_detect_outliers(self):
        url = inflation_ru_rosstat.get_page_url()
        table = inflation_ru_rosstat.get_table(url)
        outliers = inflation_ru_rosstat.detect_outliers(table)
        print(outliers)

    def test_get_main_text(self):
        url = inflation_ru_rosstat.get_page_url()
        main_text = inflation_ru_rosstat.get_main_text(url)
        print(main_text)
