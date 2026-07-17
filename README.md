# Agent_Develop

这个仓库用于记录 **AI Agent 开发学习过程**，包括学习笔记、练习代码和后续 Agent 开发项目。

---

## 学习笔记

| 笔记 | 内容 |
|------|------|
| [命令行与 JSON 学习复盘](notes/命令行与JSON学习复盘.md) | 命令行基础、JSON/YAML 语法、配置文件编写 |
| [Markdown、YAML 与 GitHub 上传复盘](notes/Markdown学习记录.md) | Markdown 语法、任务清单、README 编写、git 操作 |
| [HTTP 与 API 学习](notes/HTTP与API学习.md) | 请求响应流程、URL 组成、HTTP 方法、状态码、Header/Body、Python requests、REST 设计 |
| [FastAPI 学习笔记](notes/FastAPI学习笔记.md) | FastAPI 快速启动、路由、参数、Pydantic 校验、错误处理、综合实战 |
| [Docker 学习笔记](notes/Docker学习笔记.md) | Docker 核心概念、常用命令、Dockerfile 编写、容器化 FastAPI 服务 |
| [LLM API 调用学习笔记](notes/LLM%20API调用学习笔记.md) | API Key/Base URL、多轮对话、参数调优、结构化输出、Streaming |

---

## 学习路线

### ✅ 已完成

| 阶段 | 学习内容 | 状态 |
|------|---------|------|
| 编程与工程基础 | Python 基础语法 · Git 与 GitHub · 命令行/JSON/YAML/Markdown | ✅ 已掌握 |
| Web API 与后端基础 | HTTP 与 API 基础 · FastAPI 基础 · Docker 容器化 | ✅ 已掌握 |

### ⏳ 延后学习（用到再补）

Web API 与后端基础剩余：数据库基础（SQLite/PostgreSQL）

### 📖 学习路线（按阶段）

| 阶段 | 学习内容 | 优先级 | 说明 |
|------|---------|--------|------|
| **LLM 与 Prompt 基础** | LLM API 调用 · Prompt Engineering · 结构化输出 · Prompt & CoT · 模型微调 | ⭐⭐⭐ | 理解 LLM 工作原理，掌握提示工程和微调 |
| **Tool Call 与 ReAct** | Function Call · 手写 ReAct 循环 · 工具学习 | ⭐⭐⭐ | Agent 核心：推理 + 行动循环 |
| **Agent 运行机制** | Hello Agent 系统学习 · Skills 机制 | ⭐⭐⭐ | 理解 Agent 的完整运行原理 |
| **MCP 与工具生态** | MCP 基础 · MCP + Skills 组合实践 | ⭐⭐⭐ | 模型上下文协议，Agent 工具生态 |
| **RAG 与知识库** | RAG 基本原理 · Embedding/向量数据库 · RAG 评估优化 | ⭐⭐⭐ | 检索增强生成，让 LLM 带上下文回答 |
| **主流 Agent 框架** | LangChain 基础 · LangGraph 基础 | ⭐⭐⭐ | 当前最主流的 Agent 框架 |
| **状态、缓存与异步** | Redis 基础 · Kafka 与消息队列 | ⭐⭐ | 缓存、会话管理、异步任务 |
| **大模型进阶** | 知识编辑 · 数学推理(蒸馏) · RLHF 安全对齐 | ⭐⭐ | 深入 LLM 底层原理 |
| **Agent 工程化与评估** | Agent Memory · Agent Planning · 评估测试 · GUI Agent · 日志监控 · 安全权限 · 部署 | ⭐⭐⭐ | 将 Agent 落地为生产级服务 |
| **Mini Code Agent 实战** | 读仓库 · 编辑与测试 · 规划与上下文管理 | ⭐⭐⭐ | 端到端代码 Agent 项目 |
| **第二语言与工程视野** | Go 语言基础 | ⭐⭐ | 拓展工程视野 |

### 📊 进度总览

`
编程与工程基础    ████████████ 100% (3/3)
Web API 与后端基础 ████████████ 100% (3/5) *数据库延后*
LLM 与 Prompt 基础 ████░░░░░░░░  20% (1/5) ← 进行中
Tool Call 与 ReAct  ░░░░░░░░░░░░   0% (0/3)
Agent 运行机制     ░░░░░░░░░░░░   0% (0/2)
MCP 与工具生态     ░░░░░░░░░░░░   0% (0/2)
RAG 与知识库       ░░░░░░░░░░░░   0% (0/3)
主流 Agent 框架    ░░░░░░░░░░░░   0% (0/2)
状态、缓存与异步   ░░░░░░░░░░░░   0% (0/2)
大模型进阶         ░░░░░░░░░░░░   0% (0/3)
Agent 工程化与评估 ░░░░░░░░░░░░   0% (0/8)
Mini Code Agent 实战 ░░░░░░░░░░░░ 0% (0/3)
第二语言与工程视野  ░░░░░░░░░░░░   0% (0/1)
`

---

## 学习任务管理 API

当前学习任务：scripts/study_tasks.py（FastAPI 搭建，42 条任务，与 Notion 数据库同步）

**如何使用：**
`ash
cd F:\Python\Agent开发i-agent-practice
uvicorn scripts.study_tasks:app --reload
# 打开 http://127.0.0.1:8000/docs
`

---

## 目录结构

`	ext
Agent_Develop/
  notes/         学习笔记（含 LLM API、Docker、FastAPI、HTTP 等）
  configs/       配置文件练习
  scripts/       脚本练习（含 study_tasks.py、llm_*.py 等）
  .skills/       自定义 Skill（如 10x-learning）
  README.md
`
