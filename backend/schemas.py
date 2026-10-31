from pydantic import BaseModel, Field

class QuestionRequest(BaseModel):
    question: str = Field(min_length=3, max_length=500)

class QuestionResponse(BaseModel):
    answer: str
    intent: str
    data: object
    interpretation_method: str
