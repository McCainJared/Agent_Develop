# FastAPI 学习笔记

> **一句话总结：** FastAPI 是一个 Python Web 框架，用类型注解自动做数据校验和生成 API 文档。你写 Python 函数，它帮你变成 REST API。

---

## 大纲

- [1. 快速启动](#1-快速启动)
- [2. 路由注册：GET / POST / PUT / DELETE](#2-路由注册get--post--put--delete)
- [3. 路径参数与查询参数](#3-路径参数与查询参数)
- [4. 请求体校验：Pydantic BaseModel](#4-请求体校验pydantic-basemodel)
- [5. 错误处理](#5-错误处理)
- [6. 可选字段与部分更新（PUT 核心）](#6-可选字段与部分更新put-核心)
- [7. 综合实战：学习任务管理 API](#7-综合实战学习任务管理-api)

---

## 1. 快速启动

### 安装

```bash
pip install fastapi uvicorn
```

### 最小示例

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello Agent!"}
```

### 启动服务器

```bash
uvicorn 文件名:app --reload
# 示例
uvicorn scripts.main:app --reload
```

| 参数 | 含义 |
|------|------|
| `文件名:app` | `scripts/main.py` 中的 `app = FastAPI()` |
| `--reload` | 代码改了自动重启，开发时必加 |

### 自动文档

启动后打开：
- http://127.0.0.1:8000/docs — Swagger UI，可交互测试
- http://127.0.0.1:8000/redoc — 另一种文档风格

### 回顾思考 💭

> FastAPI 最聪明的地方：你只需要写普通 Python 函数和类型注解，它就能自动生成文档和做数据校验。**少写代码 = 少犯错。**

---

## 2. 路由注册：GET / POST / PUT / DELETE

### 基本语法

```python
@app.get("/tasks")          # 查
def get_tasks(): ...

@app.post("/tasks")         # 增
def create_task(): ...

@app.put("/tasks/{id}")     # 改
def update_task(): ...

@app.delete("/tasks/{id}")  # 删
def delete_task(): ...
```

### 必须记得

> **路由字符串必须以 `/` 开头！**
> ✅ `@app.get("/tasks")`
> ❌ `@app.get("tasks")` ← 少了斜杠，路由注册会失败

### 常用状态码

| 状态码 | 含义 | 使用场景 |
|--------|------|---------|
| 200 | 成功 | GET、PUT、DELETE |
| 201 | 创建成功 | POST |
| 404 | 找不到 | 资源 id 不存在 |
| 422 | 请求数据格式错误 | Body 校验失败 |

设置方式：
```python
from fastapi import status

@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(): ...
```

---

## 3. 路径参数与查询参数

### 路径参数（Path Parameter）

> **标识"哪个资源"**

```python
@app.get("/tasks/{task_id}")
def get_task(task_id: int):      # FastAPI 自动校验类型
    ...
```

| 访问 | task_id 的值 |
|------|-------------|
| `/tasks/3` | `3`（int） |
| `/tasks/abc` | **422 错误**（类型校验失败） |

### 查询参数（Query Parameter）

> **筛选/控制资源**

```python
@app.get("/tasks")
def get_tasks(status: str = "pending"):   # 默认值 = 不传参时的值
    ...
```

| 访问 | status 的值 |
|------|------------|
| `/tasks` | `"pending"`（走默认） |
| `/tasks?status=done` | `"done"`（覆盖默认） |

### 回顾思考 💭

> **路径参数 vs 查询参数的区分和 REST 设计完全一致：**
> - 路径参数 → "哪个资源"（`/tasks/5`）
> - 查询参数 → "什么条件"（`?status=done`）
>
> FastAPI 里，函数参数直接就是查询参数或路径参数，不需要手动解析 URL。

---

## 4. 请求体校验：Pydantic BaseModel

### 什么是 Pydantic

Pydantic 是一个数据校验库。FastAPI 用它来**自动校验请求 Body 的格式**。

### 基础用法

```python
from pydantic import BaseModel

class TaskCreate(BaseModel):
    title: str                    # 必填，必须是字符串
    status: str = "pending"       # 选填，默认值 "pending"
    note_link: str = ""           # 选填，默认空字符串

@app.post("/tasks")
def create_task(task: TaskCreate):   # FastAPI 自动校验 Body
    ...
```

### 校验规则

| 写法 | 含义 | 传参时 |
|------|------|--------|
| `title: str` | 必填，字符串 | Body 必须有 `"title"` |
| `status: str = "pending"` | 选填，默认值 | Body 可以没有 `"status"` |
| `title: str | None = None` | 可选，默认 None | 适合 PUT 部分更新 |

### 回顾思考 💭

> **`json=data`（requests 客户端） 和 `task: TaskCreate`（FastAPI 服务端）是一对镜像操作：**
> - 客户端：`json=data` → **自动把字典转成 JSON 放进 Body + 设 Content-Type**
> - 服务端：`task: TaskCreate` → **自动从 Body 读 JSON + 校验格式 + 转成 Pydantic 对象**

---

## 5. 错误处理

### 简单返回 dict（适合 demo）

```python
@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for t in tasks:
        if t["id"] == task_id:
            return t
    return {"error": "not found"}      # 状态码还是 200，不推荐
```

### 推荐：用 HTTPException

```python
from fastapi import HTTPException

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for t in tasks:
        if t["id"] == task_id:
            return t
    raise HTTPException(status_code=404, detail="Task not found")
```

这样返回的是真正的 **404 状态码**，客户端能正确识别。

---

## 6. 可选字段与部分更新（PUT 核心）

### 部分更新的关键

用 `Optional` 或 `str | None` 让所有字段可选：

```python
class TaskUpdate(BaseModel):
    title: str | None = None        # 传了就更新，没传就不动
    status: str | None = None
    note_link: str | None = None
```

### 更新逻辑

```python
@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: TaskUpdate):
    for t in tasks:
        if t["id"] == task_id:
            # 只更新传了的字段
            if task.title is not None:
                t["title"] = task.title        # = 是赋值！不是 ==
            if task.status is not None:
                t["status"] = task.status
            if task.note_link is not None:
                t["note_link"] = task.note_link
            return t
    return {"error": "not found"}
```

### 常见错误 ⚠️

| 错误写法 | 正确写法 | 原因 |
|---------|---------|------|
| `t["title"] == task.title` | `t["title"] = task.title` | `==` 是比较，`=` 才是赋值 |
| 没写 `if ... is not None` | 必须写 | 不然未传的字段会覆盖为 `None` |

### 回顾思考 💭

> **`is not None` 判断是部分更新的灵魂。**
> 如果不加判断，`title=None` 就会把原来的标题覆盖成 None，数据就丢了。

---

## 7. 综合实战：学习任务管理 API

### 完整代码结构

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

tasks = [
    {"id": 1, "title": "命令行 & JSON", "status": "done"},
    {"id": 2, "title": "HTTP & API", "status": "done"},
    {"id": 3, "title": "FastAPI", "status": "pending"},
]

# --- GET 全部 ---
@app.get("/tasks")
def get_tasks():
    return tasks

# --- GET 单个 ---
@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for t in tasks:
        if t["id"] == task_id:
            return t
    return {"error": "not found"}

# --- POST 新增 ---
class TaskCreate(BaseModel):
    title: str
    status: str = "pending"

@app.post("/tasks")
def create_task(task: TaskCreate):
    new_id = max(t["id"] for t in tasks) + 1
    new_task = {"id": new_id, "title": task.title, "status": task.status}
    tasks.append(new_task)
    return new_task

# --- PUT 更新 ---
class TaskUpdate(BaseModel):
    title: str | None = None
    status: str | None = None

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: TaskUpdate):
    for t in tasks:
        if t["id"] == task_id:
            if task.title is not None:
                t["title"] = task.title
            if task.status is not None:
                t["status"] = task.status
            return t
    return {"error": "not found"}

# --- DELETE 删除 ---
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for i, t in enumerate(tasks):
        if t["id"] == task_id:
            tasks.pop(i)
            return {"message": "deleted"}
    return {"error": "not found"}
```

---

## 速查压缩卡

```
启动：uvicorn 文件名:app --reload
文档：http://127.0.0.1:8000/docs

路由：@app.get/post/put/delete("/路径")
路径参数：/tasks/{id} → task_id: int
查询参数：?status=done → status: str = "pending"

Pydantic 校验：
  class X(BaseModel):
      name: str                # 必填
      status: str = "pending"  # 选填+默认

部分更新（PUT）：
  field: str | None = None
  if field is not None: t["field"] = field

错误：return {"error": "..."} 或 raise HTTPException(404)
```

---

*学习时间：第 9-10 次 FastAPI 学习课程*
