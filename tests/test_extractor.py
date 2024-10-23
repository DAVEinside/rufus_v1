import unittest
from rufus.extractor import ExtractorAgent
import asyncio

class TestExtractor(unittest.TestCase):
    def setUp(self):
        self.agent = ExtractorAgent()

    def test_extractor(self):
        content = "<html><body><p>Test content.</p></body></html>"
        page = ('https://example.com', content)
        extracted_data = asyncio.run(self.agent.extract_data([page]))
        self.assertIsNotNone(extracted_data)
        self.assertTrue(len(extracted_data) > 0)

if __name__ == '__main__':
    unittest.main()
