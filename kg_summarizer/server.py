from fastapi import FastAPI
from typing import Union

from reasoner_pydantic import (
    Response as PDResponse,
    Query as PDQuery
)

from kg_summarizer.trapi import GraphContainer


KG_SUM_VERSION = '0.1'

# declare the application and populate some details
app = FastAPI(
    title='Knowledge Graph Summarizer - A FastAPI UI/web service',
    version=KG_SUM_VERSION
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.post("/summarize")
async def summarize_handler(query_graph: PDQuery):#, response: PDResponse):

    # g = GraphContainer(query_graph, response, verbose=False, result_idx=0)

    return 999
