from typing import List, Optional,Literal
from fastapi import FastAPI, HTTPException,Query
from src.schemas import TaskCreate, TaskResponse

app = FastAPI(title="极简学习任务看板 API")

# 内存模拟数据库
tasks_db: List[dict] = []
current_id = 1


@app.post("/tasks", response_model=TaskResponse, summary="创建新任务")
def create_task(task_in: TaskCreate):
    """
    接收前端提交的数据，经过 Pydantic 校验通过后，
    生成 id 和 completed 状态存入内存数据库。
    """
    global current_id
    new_task = {
        "id": current_id,
        "title": task_in.title,
        "priority": task_in.priority,
        "completed": False,
    }
    tasks_db.append(new_task)
    current_id += 1
    return new_task


@app.get("/tasks", response_model=List[TaskResponse], summary="查询任务列表")
def get_tasks(completed: Optional[bool] = None,
                priority: Optional[Literal[1,2,3,4,5]] = Query(default = None,description="按优先级过滤")):
    """
    查询任务列表，支持通过 ?completed=true/false,priority=所选数字 进行过滤。
    如果不传 completed 参数，则默认返回全部,priority一样。
    """
    result = tasks_db
    if completed is not None:
        result = [task for task in result if task["completed"] == completed]
    if priority is not None:
        result = [task for task in result if task["priority"] == priority]
    return result


@app.patch("/tasks/{task_id}", response_model=TaskResponse, summary="转换任务状态")
def complete_task(task_id: int):
    """
    根据路径中的 task_id 查找任务并将其状态进行转换，true->false  false->true
    如果找不到对应 ID，主动抛出 404 异常。
    """
    for task in tasks_db:
        if task["id"] == task_id:
            task["completed"] = not task["completed"]
            return task
    # 遍历结束都没找到，抛出 404
    raise HTTPException(status_code=404, detail="任务不存在")

@app.delete("/task/{task_id}",response_model=TaskResponse,summary="删除任务")
def delete_task(task_id:int):
    """
    删除指定id的任务
    """
    for index,task in enumerate(tasks_db):
        if task["id"] == task_id:
            delete_task = tasks_db.pop(index)
            return delete_task

    raise HTTPException(status_code=404, detail="任务不存在")
