# rufus/agents.py

import logging
import asyncio
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.llms import OpenAI
from .llms import AsyncOpenAI

logger = logging.getLogger(__name__)

class PromptUnderstandingAgent:
    def __init__(self, api_key):
        self.llm = AsyncOpenAI(api_key=api_key)
        self.prompt_template = PromptTemplate(
            input_variables=["instructions"],
            template="""
            You are an AI assistant that extracts actionable items from user instructions.
            Instructions: {instructions}
            Extracted Keywords (separated by commas):
            """
        )
        self.llm_chain = LLMChain(llm=self.llm, prompt=self.prompt_template)

    async def parse_instructions(self, instructions):
        try:
            response = await self.llm_chain.arun(instructions=instructions)
            keywords = response.strip().split(',')
            return [keyword.strip() for keyword in keywords]
        except Exception as e:
            logger.error(f"Error parsing instructions: {e}")
            return []

class EvaluatorAgent:
    def __init__(self, evaluation_threshold, api_key):
        self.evaluation_threshold = evaluation_threshold
        self.llm = AsyncOpenAI(api_key=api_key)
        self.prompt_template = PromptTemplate(
            input_variables=["instructions", "data"],
            template="""
            Evaluate the relevance of the following data to the instructions on a scale from 0 to 1.
            Instructions: {instructions}
            Data: {data}
            Relevance Score (0-1):
            """
        )
        self.llm_chain = LLMChain(llm=self.llm, prompt=self.prompt_template)

    async def evaluate_and_feedback(self, extracted_data, instructions):
        scored_data = await self.evaluate_data(extracted_data, instructions)
        if self.needs_improvement(scored_data):
            feedback = self.generate_feedback(scored_data, instructions)
            return feedback
        else:
            return None

    def needs_improvement(self, scored_data):
        if not scored_data:
            return True
        average_score = sum(score for _, score in scored_data) / len(scored_data)
        return average_score < self.evaluation_threshold

    def generate_feedback(self, scored_data, instructions):
        # Identify gaps in the data and adjust crawler parameters
        new_keywords = self.extract_new_keywords(scored_data)
        feedback = {
            'new_keywords': new_keywords,
            'adjust_parameters': {
                'relevance_threshold': max(self.config.relevance_threshold - 0.1, 0.1),
                'max_depth': self.config.max_depth + 2,
                'max_pages': self.config.max_pages + 500
            }
        }
        return feedback


    def extract_new_keywords(self, scored_data):
        # Placeholder for keyword extraction logic
        return []

    async def evaluate_data(self, extracted_data, instructions):
        tasks = [self.evaluate_single_data(data, instructions) for data in extracted_data]
        scored_data = await asyncio.gather(*tasks)
        return scored_data

    async def evaluate_single_data(self, data, instructions):
        try:
            content_str = ' '.join(data['content'])
            response = await self.llm_chain.arun(instructions=instructions, data=content_str[:1000])  # Limit to 1000 chars
            score = float(response.strip())
            return (data, score)
        except Exception as e:
            logger.error(f"Error evaluating data: {e}")
            return (data, 0.0)

class OutputAgent:
    def prepare_output(self, scored_data, top_n=5):
        scored_data.sort(key=lambda x: x[1], reverse=True)
        best_data = [item[0] for item in scored_data[:top_n]]
        return best_data
