# rufus/crawler.py

import asyncio
import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import logging
import numpy as np
import traceback
import hashlib

logger = logging.getLogger(__name__)


class IntelligentCrawler:
    def __init__(self, base_url, instructions, config):
        self.base_url = base_url.rstrip('/')  # Remove trailing slash for consistency
        self.instructions = instructions
        self.config = config
        self.visited = set()
        self.relevant_pages = []
        self.url_queue = asyncio.PriorityQueue()  # Use PriorityQueue for prioritizing URLs
        self.embeddings_model = self.config.embeddings_model
        self.instructions_embedding = self.get_embedding(self.instructions)
        self.max_pages = self.config.max_pages  # Limit total pages to crawl
        self.semaphore = asyncio.Semaphore(self.config.concurrency)

    def reset(self):
        self.visited = set()
        self.relevant_pages = []
        self.url_queue = asyncio.PriorityQueue()

    async def crawl(self):
        await self.enqueue_url(self.base_url, priority=0)
        tasks = []
        while not self.url_queue.empty() and len(self.visited) < self.max_pages:
            _, url = await self.url_queue.get()
            if url in self.visited:
                continue
            tasks.append(asyncio.create_task(self.fetch_and_process(url)))
            if len(tasks) >= self.config.concurrency:
                await asyncio.gather(*tasks)
                tasks = []
        if tasks:
            await asyncio.gather(*tasks)

    async def fetch_and_process(self, url):
        self.visited.add(url)
        logger.info(f"Processing URL: {url}")
        try:
            response_text = await self.fetch(url)
            if response_text:
                if await self.is_relevant(response_text):
                    self.relevant_pages.append((url, response_text))
                await self.extract_and_enqueue_links(response_text, url)
        except Exception as e:
            logger.error(f"Error processing {url}: {e}")
            logger.debug(traceback.format_exc())

    async def fetch(self, url):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=10, allow_redirects=True) as response:
                    if response.status == 200:
                        return await response.text()
                    else:
                        logger.error(f"Non-200 response for {url}: {response.status}")
                        return None
        except Exception as e:
            logger.error(f"Error fetching {url}: {e}")
            logger.debug(traceback.format_exc())
            return None

    async def is_relevant(self, text):
        content_embedding = self.get_embedding(text)
        similarity = self.cosine_similarity(self.instructions_embedding, content_embedding)
        return similarity >= self.config.relevance_threshold

    async def extract_and_enqueue_links(self, html_content, base_url):
        soup = BeautifulSoup(html_content, 'html.parser')
        for tag in soup.find_all('a', href=True):
            href = tag['href']
            if href.startswith(('mailto:', 'tel:', 'javascript:', '#')):
                continue
            full_url = urljoin(base_url, href)
            # Normalize URL (remove fragment identifiers)
            full_url = full_url.split('#')[0]
            full_url = full_url.rstrip('/')
            if full_url not in self.visited:
                # Estimate the relevance of the link based on the link text
                link_text = tag.get_text(strip=True)
                priority = await self.estimate_link_priority(link_text)
                await self.enqueue_url(full_url, priority)


    async def estimate_link_priority(self, link_text):
        if not link_text:
            return 1.0  # Lowest priority
        link_embedding = self.get_embedding(link_text)
        similarity = self.cosine_similarity(self.instructions_embedding, link_embedding)
        # Priority queue uses lower numbers as higher priority
        return 1.0 - similarity  # Lower value means higher priority

    async def enqueue_url(self, url, priority):
        url_hash = hashlib.sha256(url.encode()).hexdigest()
        if url_hash not in self.visited:
            await self.url_queue.put((priority, url))
            logger.info(f"Enqueued URL: {url} with priority {priority}")

    # Add caching for embeddings
    def get_embedding(self, text):
        return self.embeddings_model.embed_query(text)

    # Add cosine similarity function
    def cosine_similarity(self, a, b):
        a = np.array(a)
        b = np.array(b)
        if np.linalg.norm(a) == 0 or np.linalg.norm(b) == 0:
            return 0.0
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
