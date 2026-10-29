from typing import Literal
from pydantic import BaseModel, Field, ValidationError


class SentimentAnalysis(BaseModel):
    sentiment: Literal["positive", "negative", "neutral"]
    confidence: float = Field(..., ge=0.1, le=1.0)
    keywords: list[str]


llm = '{"sentiment": "positive" , "confidence": 0.91, "keywords": ["final", "end"]}'

try:
    result = SentimentAnalysis.model_validate_json(llm)
    print(f"validation check {result.sentiment}")
    print(result.model_dump())
except ValidationError as e:
    print(f"validation failed {e.errors()}")
