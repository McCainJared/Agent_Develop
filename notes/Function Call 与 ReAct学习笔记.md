# Function Call 与 ReAct 学习笔记

> **一句话总结：** Function Call 让 LLM 输出结构化函数调用指令（JSON），程序解析后执行真实函数并返回结果；ReAct 将这一过程循环起来——"思考→行动→观察→再思考→直到能回答"。这是 Agent 的核心引擎。

---

## 大纲

- [1. Function Call 核心：tools 定义](#1-function-call-核心tools-定义)
- [2. tool_choice：LLM 何时调工具](#2-tool_choicellm-何时调工具)
- [3. tool_calls 解析：从 JSON 到真实函数](#3-tool_calls-解析从-json-到真实函数)
- [4. role="tool" 闭环：tool_call_id 的作用](#4-roletool-闭环tool_call_id-的作用)
- [5. ReAct 循环骨架](#5-react-循环骨架)
- [6. ReAct 终止条件与边界](#6-react-终止条件与边界)
- [7. 对话记忆与 Token 管理](#7-对话记忆与-token-管理)
- [Function Call 与 ReAct 速查表](#function-call-与-react-速查表)

---

## 1. Function Call 核心：tools 定义

### tools 的结构

tools 是一个列表，每个 tool 是一个包含 `type` 和 `function` 的对象。`function` 内部必须包含 `name`、`description`、`parameters`。

| 字段 | 含义 | 必填 | 类比 |
|------|------|------|------|
| **`name`** | 函数名字（LLM 靠这个名字决定调哪个） | 是 | 函数名 |
| **`description`** | 描述这个工具干什么（**没有 description，LLM 不知道什么时候该用**） | **是** | 名片上的职务说明 |
| **`parameters`** | 参数定义（LLM 按这个格式生成参数 JSON） | 是 | 函数的参数清单 |
| **`required`** | 哪些参数是必须的 | 否（但强烈建议标） | 必填项 |

### **重点记忆（易错点）**

- **`description` 不是装饰，是 LLM 判断要不要调这个工具的唯一依据**。没有 description，LLM 99% 不会调你的工具。
- **`name` 必须和真实函数名一致**，否则程序找不到对应的函数。
- **parameters 的 `properties` 里的字段名，必须和真实函数参数名一致**。

### 自测题

1. 如果不写 `description`，LLM 还会调这个工具吗？
2. `name` 写成 `"get_weather"` 但真实函数叫 `fetch_weather()`，程序会怎样？
3. 如果工具不需要参数，parameters 该怎么写？

---

## 2. tool_choice：LLM 何时调工具

### 三种模式

| 模式 | 含义 | 适用场景 |
|------|------|---------|
| **`"auto"`** | LLM **自己决定**要不要调工具（默认） | 大多数情况 |
| **`"none"`** | LLM **不调工具**，只给文本回答 | 纯对话，不需要工具 |
| **`"required"`** | LLM **必须调工具**（至少调一个） | 强制使用工具的场景 |

### **重点记忆**

> **LLM 只输出 JSON 格式的"调用指令"，不会真的执行函数。** 执行函数是程序自己的事。

### 自测题

1. 用户问"你好"，工具只有一个 `get_weather`，`tool_choice="auto"`，LLM 会调工具吗？
2. `tool_choice="required"` 时，如果用户问"你好"，LLM 会怎么做？
3. 什么时候应该用 `"none"`？

---

## 3. tool_calls 解析：从 JSON 到真实函数

### **最关键的步骤（最容易出错）**

```python
for tool_call in msg.tool_calls:
    func_name = tool_call.function.name
    func_args = json.loads(tool_call.function.arguments)  # ★ 字符串→字典
    func = available_functions[func_name]                  # 用名字查找函数
    result = func(**func_args)                             # ★ ** 解包，把字典变参数
```

### **重点记忆**

1. **`tool_call.function.arguments` 是字符串（JSON 格式），不是字典！** 必须用 `json.loads()` 转换。
2. **`**func_args` 解包：** `func_args = {"city": "北京"}` → `func(**func_args)` = `func(city="北京")`。
3. **`available_functions` 是一个字典：** `{"get_weather": get_weather, ...}`，用函数名字符串找到真实函数对象。
4. **LLM 一次可能返回多个 tool_calls**（同一个 `msg.tool_calls` 列表里有多个），循环处理每个。

---

## 4. role="tool" 闭环：tool_call_id 的作用

### **常见错误（你遇到的）**

```python
# ❌ 错误：msg 被反复 append
for tool_call in msg.tool_calls:
    messages.append(msg)    # ← 重复！导致 tool_call 和 tool 数量不匹配
    messages.append({"role": "tool", ...})

# ✅ 正确：msg 只 append 一次
messages.append(msg)        # ← 放到循环外面
for tool_call in msg.tool_calls:
    messages.append({"role": "tool", ...})
```

### **重点记忆**

- **`tool_call_id` 必须和 `tool_call.id` 完全一致**，否则 API 报 400 错误。
- **`content` 必须是字符串**。`json.dumps()` 把字典变成字符串。
- **一个 `msg.tool_calls` 有几个元素，messages 里就必须追加几个 tool 消息**，数量必须匹配！

---

## 5. ReAct 循环骨架

```
用户提问 → Thought（思考）→ Action（调工具）→ Observation（结果）→ Thought（再思考）→ Final Answer
```

---

## 6. ReAct 终止条件与边界

| 终止条件 | 结果 |
|---------|------|
| **LLM 不调工具** | 直接返回 `msg.content`（最终回答） |
| **超过 max_turns** | 返回最后一次 `msg.content`（可能为空） |

### **重点记忆**

> **max_turns 限制的是循环次数（轮次），不是工具调用个数。** 一轮里 LLM 可能调 1 个或多个工具。

---

## 7. 对话记忆与 Token 管理

| 问题 | 后果 | 解决方案 |
|------|------|---------|
| **messages 越来越长** | Token 成本飙升 | 保留最近 N 轮对话 |
| **长历史稀释注意力** | LLM 忘了开头 | 定期用 LLM 总结历史 |
| **消息里含大量 tool 结果** | Token 浪费 | 压缩 tool 结果，只保留关键信息 |

---

## Function Call 与 ReAct 速查表

| 概念 | 一句话 | 易错点 |
|------|--------|--------|
| **tools 定义** | 告诉 LLM 有哪些函数可以用 | `description` 必须写，否则 LLM 不会调 |
| **tool_choice** | "auto"=LLM 自己选 / "none"=不调 / "required"=必须调 | 默认 auto |
| **tool_calls** | LLM 返回的调用指令（JSON 格式的字符串！） | `arguments` 是字符串，需要 `json.loads()` |
| ****** 解包** | `func(**{"city": "北京"})` = `func(city="北京")` | 不写 ** 等于只传一个字典参数 |
| **tool_call_id** | 关联每次调用和对应的结果 | 写错 / 漏写 → 400 错误 |
| **role="tool"** | 把工具结果返回给 LLM | 数量必须和 tool_calls 匹配 |
| **ReAct 循环** | 反复调工具直到 LLM 能回答 | 注意终止条件和 `msg.content` 为空 |
| **`messages.append(msg)`** | 把 LLM 的回复存回历史 | **必须放在循环外面**，否则重复 append |
| **对话记忆** | 把历史 messages 传给 LLM | Token 会爆炸，需要截断或压缩 |
