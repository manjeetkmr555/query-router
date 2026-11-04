from pydantic import BaseModel, Field

from query_router.contracts import Destination


class QueryRequest(BaseModel):
    query: str = Field(min_length=1, max_length=4000)


class QueryResponse(BaseModel):
    destination: Destination
    intent: str
    confidence: float = Field(ge=0, le=1)
    reply: str
