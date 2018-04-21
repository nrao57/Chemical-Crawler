import unittest
import MainScraper

class TestChemCrawler(unittest.TestCase):

    def test_upper(self):
        path = "https://en.wikipedia.org/wiki/Carbon_monoxide"
        outputdict = MainScraper.ChemCrawler(path)
        print(outputdict)


if __name__ == '__main__':
    unittest.main()

