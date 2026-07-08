# HTTP 与 API 学习笔记

> **一句话总结：** HTTP 是客户端和服务器之间"请求和响应"的规则。API 是让程序之间按这套规则对话的接口。

---

## 大纲

- [1. HTTP 请求与响应流程](#1-http-请求与响应流程)
- [2. URL 的组成：基础地址、路径参数、查询参数](#2-url-的组成基础地址路径参数查询参数)
- [3. HTTP 方法：GET / POST / PUT / DELETE](#3-http-方法get--post--put--delete)
- [4. 状态码](#4-状态码)
- [5. Header 与 Body](#5-header-与-body)
- [6. Python requests 实战](#6-python-requests-实战)
- [7. REST API 设计规范](#7-rest-api-设计规范)

---

## 1. HTTP 请求与响应流程

### 核心流程

```
客户端 Client（浏览器/代码）
  |
  ├─ 发送 HTTP Request ──→
  |                        服务器 Server
  |                          |
  |←──── 返回 HTTP Response ──
  |
客户端 拿到数据
```

### 必须记住

> **客户端发出请求 = 你去餐厅点餐**
> **服务器返回响应 = 厨房出菜**

### 回顾思考

> 为什么要有 HTTP 这个规则？—— 为了让不同语言、不同系统写的程序能够统一地"对话"。没有这个规则，Python 写的后端和 JavaScript 写的前端就互相不认识。

---

## 2. URL 的组成：基础地址、路径参数、查询参数

### 结构拆解

```
https://jsonplaceholder.typicode.com/todos?userId=1
|                                  |      |
基础地址                            路径    查询参数（?key=value）
                                   参数
```

| 组成部分 | 含义 | 例子 |
|---------|------|------|
| 基础地址 Base URL | API 的主入口 | `https://jsonplaceholder.typicode.com` |
| 路径参数 Path Param | **标识具体资源** | `/todos`、`/todos/1` |
| 查询参数 Query Param | **筛选/排序/分页** | `?userId=1&completed=false` |

### 必须记住

> **没有路径参数，服务器不知道你要什么资源**
> **没有查询参数，服务器返回全部（或默认）**

### 回顾思考

> 路径参数和查询参数怎么区分？—— 路径参数回答"哪个资源"，查询参数回答"什么条件"。
> `/todos/1` → "我要 todo 列表里的第 1 个"
> `/todos?userId=1` → "我要 todo 列表里 userId 等于 1 的那些"

## 3. HTTP 方法：GET / POST / PUT / DELETE

### 四大方法速查

| 方法 | 动作 | 通俗理解 | Body 情况 |
|------|------|---------|----------|
| **GET** | **获取**数据 | 看菜单，不点菜 | 无 Body |
| **POST** | **创建**新数据 | 点一道菜，厨房新增 | 有 Body（新菜的数据） |
| **PUT** | **替换**已有数据 | 把菜端回去，重新做一份 | 有 Body（完整替换） |
| **DELETE** | **删除**数据 | 把菜撤掉 | 通常无 Body |

### 必须记住

> **GET 只读，POST 新增，PUT 全量替换，DELETE 删除**
> **POST 和 PUT 的区别：POST 是新增，服务器给你新 ID；PUT 是替换已有资源**

### 回顾思考

> 同样传 body，POST 和 PUT 用法上什么区别？
> - POST `/todos` → 创建一个新 todo，服务器自动分配 id
> - PUT `/todos/5` → 把 id=5 的 todo 整个替换掉（必须提供完整的字段）
> 实战中，PUT 需要你知道目标资源的 id，POST 不需要。

---

## 4. 状态码

### 核心五类

| 范围 | 含义 | 通俗理解 |
|------|------|---------|
| **1xx** | 信息，服务器还在处理 | 厨房说"收到，正做着呢" |
| **2xx** | **成功** | 菜做好了端上桌 |
| **3xx** | 重定向，需要去别处找 | "这道菜在隔壁餐厅" |
| **4xx** | **客户端错误** | 你点错了，菜单上没有这道菜 |
| **5xx** | **服务器错误** | 厨房炸了，不关你事 |

### 必须记住的常用码

| 状态码 | 含义 | 场景 |
|--------|------|------|
| **200** | OK，请求成功 | GET 拿到数据 |
| **201** | Created，创建成功 | POST 新建资源后返回 |
| **401** | Unauthorized，未登录 | 没带 token |
| **403** | Forbidden，禁止访问 | 登录了但没权限 |
| **404** | Not Found，找不到 | URL 写错了，或资源已被删 |
| **500** | Internal Server Error | 服务器内部出 bug 了 |

### 回顾思考

> 删除了 `/todos/3` 后再 GET `/todos/3`，返回什么？—— **404**，因为客户端去请求了一个不存在的资源。
> 4xx 是客户端的问题，5xx 是服务器的问题。**调试时先看状态码，4 字头检查你的请求，5 字头等后端修。**

---

## 5. Header 与 Body

### Header（信封封面）

> **Header 是"描述信息"，不是"用户内容"**

```
Content-Type: application/json    → 告诉对方 Body 是 JSON 格式
Authorization: Bearer sk-xxx      → 告诉对方"我是谁"
```

### Body（信封里的信）

> **Body 是实际传输的数据**

```json
{
  "title": "学习 HTTP",
  "completed": false
}
```

### Content-Type 的作用

```
Content-Type: application/json

服务器看到→"Body 是 JSON，我用 JSON 解析器去读"
如果没有 Content-Type → 服务器不知道该怎么解析 Body
```

### 必须记住

> **`json=data` 自动做两件事：**
> 1. 把 `data` 字典转成 JSON 放进 Body
> 2. 自动设 `Content-Type: application/json`
>
> 等于下面两行：
> ```python
> r = requests.post(url, data=json.dumps(data), headers={"Content-Type": "application/json"})
> ```

### 回顾思考

> 常见的真实 Header 有哪些？
> - `Content-Type` → 描述 body 的格式（JSON、表单、纯文本）
> - `Authorization` → 身份认证（Bearer token、API Key）
> - `Accept` → 客户端想要什么格式的响应
> - `User-Agent` → 告诉服务器你是谁（浏览器、Python 脚本等）

---

## 6. Python requests 实战

### 最常用的写法

```python
import requests

# GET 请求
r = requests.get("https://jsonplaceholder.typicode.com/todos?userId=1")
data = r.json()           # 解析 JSON → Python 字典或列表
print(r.status_code)      # 打印状态码，比如 200

# POST 请求（新增数据）
new_todo = {"title": "学习API", "completed": False}
r = requests.post("https://jsonplaceholder.typicode.com/todos", json=new_todo)
print(r.status_code)      # 201 Created
```

### JSON 解析规则（必须背熟）

> **JSON 顶层是什么，`r.json()` 就是什么**

| API 路径 | JSON 顶层 | Python 类型 | 访问方式 |
|----------|-----------|-------------|---------|
| `/todos` | `[...]` 数组 | **list** | `data[0]`、`data[1]` |
| `/todos/1` | `{...}` 对象 | **dict** | `data["title"]` |
| `/todos?userId=1` | `[...]` 数组 | **list** | `data[0]["title"]` |

### 数据筛选模板

```python
r = requests.get("https://jsonplaceholder.typicode.com/todos?userId=1")
data = r.json()

# 筛选未完成的 todo
for todo in data:
    if not todo["completed"]:
        print(todo["title"])
```

### 回顾思考

> 为什么 `todos?userId=1` 返回的是 list 不是 dict？
> 因为查询参数只是从完整列表里**过滤**，顶层结构没变——原接口 `/todos` 本身就是返回数组。
> `r.json()` 的返回值类型 = **JSON 顶层的数据类型**，跟查询条件无关。

---

## 7. REST API 设计规范

### 铁律一：URL 只有名词，没有动词

| 符合 REST | 反模式 |
|-------------|----------|
| `GET /users` | `GET /getUsers` |
| `POST /users` | `POST /createUser` |
| `DELETE /users/5` | `GET /deleteUser?id=5` |

### 铁律二：嵌套路径体现资源归属

```
资源 A 下有资源 B →  /A/{a_id}/B
```

| 操作 | 正确写法 |
|------|---------|
| 用户 3 的文章 | `GET /users/3/posts` |
| 文章 10 的评论 | `GET /posts/10/comments` |
| 删除文章 10 的评论 5 | `DELETE /posts/10/comments/5` |

### 铁律三：路径参数 vs 查询参数

```
路径参数 = "这是哪个资源"          → /users/5，/todos/1
查询参数 = "控制/筛选资源"         → ?page=2，?status=active
```

### 常见失误自查

| 错误 | 原因 | 正确 |
|------|------|------|
| `GET /getUsers` | 含动词 | `GET /users` |
| `DELETE /users/posts/5` | 跳级 | `DELETE /posts/5` |
| `POST /todos` 没传 body | 创建需要数据 | 传 `json=data` |
| `PUT /todos` 没指定 id | 替换需要目标 | `PUT /todos/5` |

### 回顾思考

> REST 设计的核心思维：把系统里的"东西"（用户、文章、评论）都看作**资源**。
> 你只是在对这些资源做：查、增、换、删。
> 所以路径只要写资源的名字（名词），方法（动词）交给 HTTP 方法。

---

## 速查压缩卡

```
HTTP 请求流程：客户端 → 请求 → 服务器 → 响应 → 客户端

URL 三板斧：基础地址 + 路径参数 + 查询参数

方法：GET 查 / POST 增 / PUT 替 / DELETE 删

状态码：200 成功 / 201 创建 / 401 未登录 / 403 无权限 / 404 找不到 / 500 服务器炸

JSON 解析：JSON 数组 → list，JSON 对象 → dict，顶层决定类型

REST 设计：URL 只有名词无动词，嵌套体现归属，路径标识资源查询控制条件
```

---

*学习时间：第 1-8 次 HTTP/API 学习课程*
