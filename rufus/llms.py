# rufus/llms.py

import os
from dotenv import load_dotenv
from langchain_community.llms import OpenAI
import asyncio

load_dotenv()

class AsyncOpenAI(OpenAI):
    def __init__(self, api_key=None, **kwargs):
        api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OpenAI API key not found. Please set OPENAI_API_KEY in your environment variables or .env file.")
        super().__init__(openai_api_key=api_key, **kwargs)

    async def arun(self, *args, **kwargs):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None, lambda: self.run(*args, **kwargs)
        )
