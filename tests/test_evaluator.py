import unittest
from rufus.agents import EvaluatorAgent
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

class TestEvaluator(unittest.TestCase):
    def setUp(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key not found. Please set OPENAI_API_KEY in your environment variables.")
        self.evaluator_agent = EvaluatorAgent(evaluation_threshold=0.7, api_key=self.api_key)

    def test_evaluator(self):
        extracted_data = [{'content': ['Sample data']}]
        instructions = "Sample instructions"
        scored_data = asyncio.run(self.evaluator_agent.evaluate_data(extracted_data, instructions))
        self.assertIsInstance(scored_data, list)
        self.assertTrue(len(scored_data) > 0)

if __name__ == '__main__':
    unittest.main()
