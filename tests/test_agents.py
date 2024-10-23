import unittest
from rufus.agents import PromptUnderstandingAgent, EvaluatorAgent
from rufus.config import RufusConfig
import asyncio

class TestAgents(unittest.TestCase):
    def setUp(self):
        self.api_key = 'test_api_key'
        self.prompt_agent = PromptUnderstandingAgent(api_key=self.api_key)
        self.evaluator_agent = EvaluatorAgent(evaluation_threshold=0.7, api_key=self.api_key)

    def test_prompt_understanding(self):
        instructions = "Find information about product features and customer FAQs."
        keywords = asyncio.run(self.prompt_agent.parse_instructions(instructions))
        self.assertIsInstance(keywords, list)
        self.assertTrue(len(keywords) > 0)

    def test_evaluator_agent(self):
        extracted_data = [{'content': ['Sample data']}]
        instructions = "Sample instructions"
        scored_data = asyncio.run(self.evaluator_agent.evaluate_data(extracted_data, instructions))
        self.assertIsInstance(scored_data, list)
        self.assertTrue(len(scored_data) > 0)

if __name__ == '__main__':
    unittest.main()
