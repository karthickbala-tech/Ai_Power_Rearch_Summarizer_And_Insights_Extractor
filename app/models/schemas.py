from pydantic import BaseModel
from typing import List

class SummarizeRequest(BaseModel):
    paper_id: str
    length: str = "medium"

class InsightRequest(BaseModel):
    paper_id: str
    questions: List[str]