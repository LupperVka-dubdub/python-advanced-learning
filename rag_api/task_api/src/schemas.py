from pydantic import BaseModel, Field

# 1. 前端创建任务时传进来的数据格式（请求体）
class TaskCreate(BaseModel):
    # min_length=1 拒绝空字符串，description 会直接显示在 Swagger 网页文档里
    title: str = Field(..., min_length=1, description="任务标题，不能为空")
    # ge=1 (>=1), le=5 (<=5)，限制优先级只能在 1 到 5 之间，默认值为 1
    priority: int = Field(default=1, ge=1, le=5, description="优先级 1-5")

# 2. 后端返回给前端的完整任务格式（响应体）
class TaskResponse(BaseModel):
    id: int
    title: str
    priority: int
    completed: bool = False