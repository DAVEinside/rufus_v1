# rufus/config.py

from langchain.embeddings import OpenAIEmbeddings

class RufusConfig:
    def __init__(
        self,
        max_depth=10,
        extraction_granularity='paragraph',
        evaluation_threshold=0.7,
        relevance_threshold=0.3,
        embeddings_model=None,
        max_pages=1000,
        concurrency=10,
    ):
        self.max_depth = max_depth
        self.extraction_granularity = extraction_granularity
        self.evaluation_threshold = evaluation_threshold
        self.relevance_threshold = relevance_threshold
        self.embeddings_model = embeddings_model
        self.max_pages = max_pages
        self.concurrency = concurrency
