# ============================================================
# 导入依赖
# ============================================================
# FastAPI: Web 框架核心，用来创建应用实例和注册路由
from fastapi import FastAPI
# BaseModel: Pydantic 的数据模型基类，定义请求体的结构和校验规则
from pydantic import BaseModel

# ============================================================
# 创建 FastAPI 应用实例
# ============================================================
# 运行方式: uvicorn study_tasks:app --reload
app = FastAPI()

# ============================================================
# 模拟数据库
# ============================================================
# tasks 是一个存在内存里的 Python 列表，程序重启数据就丢失。
# 每条任务有四个字段:
#   id        —— 数字，唯一标识
#   title     —— 字符串，任务标题
#   status    —— 字符串，任务状态 ("done" 已完成 / "pending" 待办)
#   note_link —— 字符串，关联的学习笔记文件路径
tasks = [
    {"id": 1, "title": "命令行 & JSON",   "status": "done",    "note_link": "notes/命令行与JSON学习复盘.md"},
    {"id": 2, "title": "HTTP & API",      "status": "done",    "note_link": "notes/HTTP 与 API学习.md"},
    {"id": 3, "title": "学习FastAPI",      "status": "done",    "note_link": "notes/FastAPI学习笔记.md"},
    {"id": 4, "title": "Python基础语法巩固",  "status": "pending", "note_link": null},
    {"id": 5, "title": "Skills/MCP/Prompt/Function Call", "status": "pending", "note_link": null},
    {"id": 6, "title": "手动搭建ReAct循环",   "status": "pending", "note_link": null},
    {"id": 7, "title": "提示学习与思维链(CoT)", "status": "pending", "note_link": null},
    {"id": 8, "title": "模型微调与部署",     "status": "pending", "note_link": null},
    {"id": 9, "title": "RAG基本原理",       "status": "pending", "note_link": null},
    {"id": 10, "title": "LangChain & LangGraph", "status": "pending", "note_link": null},
    {"id": 11, "title": "Redis",           "status": "pending", "note_link": null},
    {"id": 12, "title": "消息队列Kafka",     "status": "pending", "note_link": null},
    {"id": 13, "title": "知识编辑(Knowledge Editing)", "status": "pending", "note_link": null},
    {"id": 14, "title": "数学推理(蒸馏mini-R1)", "status": "pending", "note_link": null},
    {"id": 15, "title": "工具学习(Tool Learning)", "status": "pending", "note_link": null},
    {"id": 16, "title": "GUI Agent",        "status": "pending", "note_link": null},
    {"id": 17, "title": "智能体安全",        "status": "pending", "note_link": null},
    {"id": 18, "title": "RLHF安全对齐",     "status": "pending", "note_link": null},
    {"id": 19, "title": "mini-code开发",    "status": "pending", "note_link": null},
]

# ============================================================
# 路由 ① GET /tasks —— 获取全部任务列表
# ============================================================
# 示例: curl http://127.0.0.1:8000/tasks
# 响应: 上面 tasks 列表的完整 JSON
@app.get("/tasks")
def get_tasks():
    return tasks  # FastAPI 自动 Python 列表 → JSON 数组


# ============================================================
# 路由 ② GET /tasks/{task_id} —— 根据 ID 获取单个任务
# ============================================================
# {task_id} 是路径参数，FastAPI 自动从 URL 提取并转为整数。
# 示例: curl http://127.0.0.1:8000/tasks/1
# 成功 → {"id":1,"title":"命令行 & JSON","status":"done",...}
# 失败 → {"error":"not found"}
@app.get("/tasks/{task_id}")
def get_task_id(task_id: int):
    for t in tasks:
        if t["id"] == task_id:
            return t                   # 找到了 → 返回该条
    return {"error": "not found"}      # 没找到 → 返回错误


# ============================================================
# 请求体模型 ① TaskCreate —— 创建任务时的请求体结构
# ============================================================
# 客户端 POST 时必须在 JSON 中提供:
#   title     —— 必填，字符串
#   note_link —— 必填，字符串
#   status    —— 可选，字符串，不传则默认 "pending"
class TaskCreate(BaseModel):
    title: str                     # 必填
    status: str = "pending"        # 可选，默认 "pending"
    note_link: str                 # 必填


# ============================================================
# 路由 ③ POST /tasks —— 新增一条任务
# ============================================================
# FastAPI 自动把请求体 JSON 解析为 TaskCreate 对象 (task)，
# 然后通过 task.title / task.status / task.note_link 访问各字段。
#
# 示例: curl -X POST http://127.0.0.1:8000/tasks \
#         -H "Content-Type: application/json" \
#         -d '{"title":"学Docker","note_link":"notes/docker.md"}'
# 响应: {"id":4,"title":"学Docker","status":"pending","note_link":"notes/docker.md"}
@app.post("/tasks")
def create_task(task: TaskCreate):
    # 自增 ID: 取当前最大 id + 1
    new_id = max(t["id"] for t in tasks) + 1

    # 构造新任务字典，字段值来自请求体
    new_task = {
        "id": new_id,
        "title": task.title,
        "status": task.status,
        "note_link": task.note_link,
    }

    # 追加到内存列表
    tasks.append(new_task)
    return new_task  # 返回新创建的任务（FastAPI 自动转 JSON）


# ============================================================
# 请求体模型 ② TaskUpdate —— 更新任务时的请求体结构
# ============================================================
# 与 TaskCreate 的关键区别：所有字段都是可选的！
#
# str | None = None 的含义:
#   1. str | None  —— 类型是"字符串 或 None"
#   2. = None      —— 默认值是 None（客户端不传这个字段时就是 None）
#
# 这样客户端可以只传想修改的字段，实现"部分更新"（PATCH 风格）:
#   只改状态 → {"status": "done"}
#   只改标题 → {"title": "新标题"}
#   全改     → {"title": "新标题", "status": "done", "note_link": "新路径"}
class TaskUpdate(BaseModel):
    title: str | None = None       # 可选，传了则更新标题
    status: str | None = None      # 可选，传了则更新状态
    note_link: str | None = None   # 可选，传了则更新笔记链接


# ============================================================
# 路由 ④ PUT /tasks/{task_id} —— 更新一条任务（部分更新）
# ============================================================
# 只更新客户端传了的字段，没传的字段保持原值不变。
#
# 示例: curl -X PUT http://127.0.0.1:8000/tasks/3 \
#         -H "Content-Type: application/json" \
#         -d '{"status":"done"}'
# 这条请求只把 id=3 的任务状态改成 "done"，title 和 note_link 不动。
@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: TaskUpdate):
    for t in tasks:
        if t["id"] == task_id:
            # ↓ 只有客户端传了该字段（值不为 None）时才更新
            if task.title is not None:
                t["title"] = task.title

            if task.status is not None:
                t["status"] = task.status

            if task.note_link is not None:
                t["note_link"] = task.note_link

            return t                  # 返回更新后的完整任务

    return {"error": "not found"}     # 没找到对应的 id


# ============================================================
# 路由 ⑤ DELETE /tasks/{task_id} —— 根据 ID 删除一条任务
# ============================================================
# 示例: curl -X DELETE http://127.0.0.1:8000/tasks/2
# 成功 → {"message":"删除成功"}
# 失败 → {"error":"未找到，删除错误"}
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    # enumerate 同时拿到索引 i 和元素 t，方便用 pop(i) 删除
    for i, t in enumerate(tasks):
        if t["id"] == task_id:
            tasks.pop(i)                    # 按索引移除
            return {"message": "删除成功"}   # 删除成功

    return {"error": "未找到，删除错误"}      # 没找到对应 id
