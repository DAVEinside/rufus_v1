# rufus/extractor.py

import asyncio
from bs4 import BeautifulSoup
import logging
import re
import json

logger = logging.getLogger(__name__)

class ExtractorAgent:
    def __init__(self, granularity='paragraph'):
        self.granularity = granularity

    async def extract_data(self, pages):
        tasks = [self.extract_from_page(url, content) for url, content in pages]
        extracted_data = await asyncio.gather(*tasks)
        return [data for data in extracted_data if data]

    async def extract_from_page(self, url, content):
        try:
            text = self.extract_text(content)
            if self.granularity == 'sentence':
                texts = self.extract_sentences(text)
            else:
                texts = self.extract_paragraphs(text)
            structured_data = {
                'url': url,
                'content': texts
            }
            return structured_data
        except Exception as e:
            logger.error(f"Error extracting from {url}: {e}")
            return None

    def extract_text(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        # Remove unwanted tags
        for script_or_style in soup(["script", "style", "header", "footer", "nav", "aside"]):
            script_or_style.decompose()
        text = soup.get_text(separator=' ')
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    def extract_sentences(self, text):
        import nltk
        nltk.download('punkt', quiet=True)
        from nltk.tokenize import sent_tokenize
        sentences = sent_tokenize(text)
        return [sentence.strip() for sentence in sentences if sentence.strip()]

    def extract_paragraphs(self, text):
        paragraphs = text.split('\n\n')
        paragraphs = [para.strip() for para in paragraphs if para.strip()]
        return paragraphs
