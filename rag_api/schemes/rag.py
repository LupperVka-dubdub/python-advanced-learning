from pydantic import BaseModel,Field
from typing import List

class Queryrequest(BaseModel):
    query:str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="用户提问内容"
        examples=["FastAPI如何实现流式响应?"]
    )
    top_k:int = Field(
        default = 3,
        ge=1,
        le=10,
        description="召回参考切片数量(1-10)"
    )

class QueryResponse(BaseModel):
    answer:str = Field(
        ...,
        description="生成的回答内容"
    )
    sources:List = Field(
        default=None,
        description="参考的文档来源"
    )
    model_name:str = Field(
        default="gemini-pro"
    )

