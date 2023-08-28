"""Setup file for reasoner package."""
from pathlib import Path

from setuptools import setup

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="kg-summarizer",
    version="0.1",
    author="Joey Richardson",
    author_email="richardson.joey.b@gmail.com",
    url="https://github.com/jrichardson97/kg-summarizer",
    description="Knowledge graph summarization using large language models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["kg_summarizer"],
)