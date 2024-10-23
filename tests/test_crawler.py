import unittest
from rufus.crawler import IntelligentCrawler
from rufus.config import RufusConfig
import asyncio

class TestCrawler(unittest.TestCase):
    def setUp(self):
        self.config = RufusConfig(max_depth=1)
        self.crawler = IntelligentCrawler('https://example.com', ['example'], self.config)

    def test_crawler(self):
        asyncio.run(self.crawler.crawl('https://example.com', depth=0))
        self.assertIsInstance(self.crawler.relevant_pages, list)

if __name__ == '__main__':
    unittest.main()
