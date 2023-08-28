from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

from reasoner_pydantic import Response as PDResponse

from kg_summarizer.trapi import GraphContainer
from kg_summarizer.ai import generate_response

class LLMParameters(BaseModel):
    gpt_model: str
    temperature: Optional[float] = 0.0

class TrapiParameters(BaseModel):
    result_idx: Optional[int] = 0

class Parameters(BaseModel):
    llm: Optional[LLMParameters]
    trapi: Optional[TrapiParameters]

class AbstractItem(BaseModel):
    abstract: str
    parameters: Parameters

class ResponseItem(BaseModel):
    response: PDResponse
    parameters: Parameters


KG_SUM_VERSION = '0.1'

# declare the application and populate some details
app = FastAPI(
    title='Knowledge Graph Summarizer - A FastAPI UI/web service',
    version=KG_SUM_VERSION
)

@app.post("/summarize/abstract")
async def summarize_abstract_handler(item: AbstractItem):
    system_prompt = f"""
    You are a pharmacology researcher summarizing publication abstracts. Condense the follow abstract to a single sentence.
    """

    summary = generate_response(
        system_prompt, 
        item.abstract, 
        item.parameters.llm.gpt_model,
        item.parameters.llm.temperature,
    )
    return summary

@app.post("/summarize/edges")
async def summarize_edges_handler(item: ResponseItem):

    g = GraphContainer(
        item.response, 
        verbose=False, 
        result_idx=item.parameters.trapi.result_idx
    )

    return 999
