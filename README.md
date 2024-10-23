# Rufus

Rufus is an intelligent web data extraction tool designed to prepare web data for use in Retrieval-Augmented Generation (RAG) agents. It intelligently crawls websites based on user-defined prompts, extracts and synthesizes data into structured documents, and provides clean, ready-to-use data for downstream LLM applications.

## Features

- **Intelligent Web Crawling**: Crawls websites based on user prompts, handling nested links and complex structures.
- **Data Extraction**: Extracts and synthesizes relevant data into structured formats.
- **Multi-Agent System**: Uses LangChain to create a multi-agent system where each agent handles a specific task.
- **Concurrency**: Agents run concurrently to improve performance.
- **Feedback Loop**: Evaluator Agent influences Crawler and Extractor Agents to refine outputs.
- **Robust Error Handling**: Each agent includes error handling and logging.
- **Configurable Parameters**: Adjust parameters like crawling depth, extraction granularity, and evaluation thresholds.

## Installation

```bash
pip install -r requirements.txt

Usage

from rufus import RufusClient, RufusConfig

config = RufusConfig(
    max_depth=3,
    extraction_granularity='sentence',
    evaluation_threshold=0.8
)

client = RufusClient(api_key='YOUR_OPENAI_API_KEY', config=config)

instructions = "We're making a chatbot for the HR department in San Francisco."

documents = client.run("https://sfgov.org", instructions)

print(documents)


