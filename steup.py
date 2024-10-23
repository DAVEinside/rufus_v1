from setuptools import setup, find_packages

setup(
    name='rufus',
    version='0.2.0',
    description='Intelligent web data extraction tool for RAG systems',
    author='nimit dave',
    packages=find_packages(),
    install_requires=[
        'aiohttp',
        'asyncio',
        'beautifulsoup4',
        'langchain>=0.2.0',
        'langchain-community',
        'openai',
        'requests',
        'tqdm',
        'spacy',
        'python-dotenv',
        'nltk',
        'numpy',
    ],
    entry_points={
        'console_scripts': [
            'rufus = rufus.app:main',
        ],
    },
)
