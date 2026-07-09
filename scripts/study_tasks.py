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
    {"id": 1,  "title": "Python 基础语法",                    "status": "done",    "stage": "编程与工程基础",     "note_link": null},
    {"id": 2,  "title": "Git 与 GitHub 基础",                 "status": "done",    "stage": "编程与工程基础",     "note_link": null},
    {"id": 3,  "title": "命令行、JSON、YAML、Markdown",        "status": "done",    "stage": "编程与工程基础",     "note_link": null},

    {"id": 4,  "title": "HTTP 与 API 基础",                   "status": "done",    "stage": "Web API 与后端基础",  "note_link": null},
    {"id": 5,  "title": "FastAPI 基础",                       "status": "done",    "stage": "Web API 与后端基础",  "note_link": null},
    {"id": 6,  "title": "数据库基础：SQLite/PostgreSQL",       "status": "pending", "stage": "Web API 与后端基础",  "note_link": null},
    {"id": 7,  "title": "Docker 基础",                        "status": "pending", "stage": "Web API 与后端基础",  "note_link": null},

    {"id": 8,  "title": "LLM API 调用",                       "status": "pending", "stage": "LLM 与 Prompt 基础",  "note_link": null},
    {"id": 9,  "title": "Prompt Engineering",                 "status": "pending", "stage": "LLM 与 Prompt 基础",  "note_link": null},
    {"id": 10, "title": "结构化输出与解析",                    "status": "pending", "stage": "LLM 与 Prompt 基础",  "note_link": null},
    {"id": 11, "title": "提示学习与思维链 (Prompt and CoT)",   "status": "pending", "stage": "LLM 与 Prompt 基础",  "note_link": null},
    {"id": 12, "title": "模型微调与部署 (Fine-tuning)",       "status": "pending", "stage": "LLM 与 Prompt 基础",  "note_link": null},

    {"id": 13, "title": "Function Call / Tool Call",           "status": "pending", "stage": "Tool Call 与 ReAct",  "note_link": null},
    {"id": 14, "title": "手写 ReAct 循环",                     "status": "pending", "stage": "Tool Call 与 ReAct",  "note_link": null},
    {"id": 15, "title": "工具学习 (Tool Learning)",            "status": "pending", "stage": "Tool Call 与 ReAct",  "note_link": null},

    {"id": 16, "title": "Hello Agent 系统学习",                "status": "pending", "stage": "Agent 运行机制",     "note_link": null},
    {"id": 17, "title": "Skills 机制",                         "status": "pending", "stage": "Agent 运行机制",     "note_link": null},

    {"id": 18, "title": "MCP 基础",                            "status": "pending", "stage": "MCP 与工具生态",    "note_link": null},
    {"id": 19, "title": "MCP + Skills 组合实践",               "status": "pending", "stage": "MCP 与工具生态",    "note_link": null},

    {"id": 20, "title": "RAG 基本原理",                        "status": "pending", "stage": "RAG 与知识库",      "note_link": null},
    {"id": 21, "title": "Embedding 与向量数据库",              "status": "pending", "stage": "RAG 与知识库",      "note_link": null},
    {"id": 22, "title": "RAG 评估与优化",                      "status": "pending", "stage": "RAG 与知识库",      "note_link": null},

    {"id": 23, "title": "LangChain 基础",                      "status": "pending", "stage": "主流 Agent 框架",   "note_link": null},
    {"id": 24, "title": "LangGraph 基础",                      "status": "pending", "stage": "主流 Agent 框架",   "note_link": null},

    {"id": 25, "title": "Redis 基础",                          "status": "pending", "stage": "状态、缓存与异步",  "note_link": null},
    {"id": 26, "title": "Kafka 与消息队列",                    "status": "pending", "stage": "状态、缓存与异步",  "note_link": null},

    {"id": 27, "title": "知识编辑 (Knowledge Editing)",        "status": "pending", "stage": "大模型进阶",        "note_link": null},
    {"id": 28, "title": "数学推理 (蒸馏 mini-R1)",             "status": "pending", "stage": "大模型进阶",        "note_link": null},
    {"id": 29, "title": "RLHF 安全对齐",                      "status": "pending", "stage": "大模型进阶",        "note_link": null},

    {"id": 30, "title": "Agent Memory 设计",                   "status": "pending", "stage": "Agent 工程化与评估", "note_link": null},
    {"id": 31, "title": "Agent Planning",                      "status": "pending", "stage": "Agent 工程化与评估", "note_link": null},
    {"id": 32, "title": "Agent 评估与测试",                    "status": "pending", "stage": "Agent 工程化与评估", "note_link": null},
    {"id": 33, "title": "GUI Agent",                           "status": "pending", "stage": "Agent 工程化与评估", "note_link": null},
    {"id": 34, "title": "日志、监控与调试",                    "status": "pending", "stage": "Agent 工程化与评估", "note_link": null},
    {"id": 35, "title": "智能体安全 (Agent Safety)",           "status": "pending", "stage": "Agent 工程化与评估", "note_link": null},
    {"id": 36, "title": "安全、权限与成本控制",                "status": "pending", "stage": "Agent 工程化与评估", "note_link": null},
    {"id": 37, "title": "部署一个 Agent 服务",                 "status": "pending", "stage": "Agent 工程化与评估", "note_link": null},

    {"id": 38, "title": "mini-code Agent：读仓库",             "status": "pending", "stage": "Mini Code Agent 实战", "note_link": null},
    {"id": 39, "title": "mini-code Agent：编辑与测试",         "status": "pending", "stage": "Mini Code Agent 实战", "note_link": null},
    {"id": 40, "title": "mini-code Agent：规划与上下文管理",   "status": "pending", "stage": "Mini Code Agent 实战", "note_link": null},

    {"id": 41, "title": "Go 语言基础",                         "status": "pending", "stage": "第二语言与工程视野", "note_link": null},

    {"id": 42, "title": "S",                                   "status": "pending", "stage": "Agent 运行机制",     "note_link": null},
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
