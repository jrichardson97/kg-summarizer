# kg-summarizer
Knowledge graph summarization using LLMs with a FastAPI interface

# Create Environment
python -m venv venv
venv\Scripts\activate
pip install -r .\requirements.txt

# Start FastAPI/Uvicorn Server
uvicorn main:app --reload

