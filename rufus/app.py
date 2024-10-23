# rufus/app.py

import os
from dotenv import load_dotenv
from .agents import PromptUnderstandingAgent, EvaluatorAgent, OutputAgent
from .crawler import IntelligentCrawler
from .extractor import ExtractorAgent
from .config import RufusConfig
import asyncio
from langchain.embeddings import OpenAIEmbeddings

load_dotenv()

class RufusClient:
    def __init__(self, api_key=None, config=None):
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key not found. Please set OPENAI_API_KEY in your environment variables or .env file.")
        self.config = config if config else RufusConfig()
        self.config.embeddings_model = self.config.embeddings_model or OpenAIEmbeddings(openai_api_key=self.api_key)
        self.prompt_agent = PromptUnderstandingAgent(self.api_key)
        self.evaluator_agent = EvaluatorAgent(self.config.evaluation_threshold, self.api_key)
        self.extractor_agent = ExtractorAgent(self.config.extraction_granularity)
        self.output_agent = OutputAgent()

    async def scrape(self, url, instructions):
        keywords = await self.prompt_agent.parse_instructions(instructions)
        self.config.instructions = instructions
        crawler_agent = IntelligentCrawler(url, instructions, self.config)
        await crawler_agent.crawl()
        extracted_data = await self.extractor_agent.extract_data(crawler_agent.relevant_pages)
        feedback = await self.evaluator_agent.evaluate_and_feedback(extracted_data, instructions)
        if feedback:
            # Update parameters based on feedback
            keywords.extend(feedback.get('new_keywords', []))
            crawler_agent.config.max_depth = feedback.get('adjust_parameters', {}).get('max_depth', crawler_agent.config.max_depth)
            # Re-run crawling and extraction with updated parameters
            crawler_agent.reset()
            await crawler_agent.crawl()
            extracted_data = await self.extractor_agent.extract_data(crawler_agent.relevant_pages)
        # Final evaluation
        scored_data = await self.evaluator_agent.evaluate_data(extracted_data, instructions)
        output = self.output_agent.prepare_output(scored_data)
        return output

    def run(self, url, instructions):
        return asyncio.run(self.scrape(url, instructions))

def main():
    import argparse

    parser = argparse.ArgumentParser(description='Run Rufus web data extraction.')
    parser.add_argument('url', type=str, help='The starting URL for crawling.')
    parser.add_argument('instructions', type=str, help='User-defined instructions for data extraction.')
    args = parser.parse_args()

    client = RufusClient()
    documents = client.run(args.url, args.instructions)
    print(documents)
