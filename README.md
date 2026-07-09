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

---

## 学习路线

### 基础阶段 ✅

- [x] 命令行 & JSON & YAML & Markdown
- [x] HTTP & API
- [x] FastAPI（学习任务管理 API v1）

### AI Agent 核心阶段

| # | 学习主题 | 优先级 | 说明 |
|---|---------|--------|------|
| 1 | Python 基础语法巩固 | ⭐⭐⭐ | 类型注解、装饰器、异步、生成器 |
| 2 | Skills / MCP / Prompt / Function Call | ⭐⭐⭐ | Agent 四大核心概念 |
| 3 | 手动搭建 ReAct 循环 | ⭐⭐⭐ | 理解 Reasoning + Acting 的核心机制 |
| 4 | RAG 基本原理 | ⭐⭐⭐ | 检索增强生成，让 LLM 带上下文回答 |
| 5 | LangChain & LangGraph | ⭐⭐⭐ | 当前最主流的 Agent 框架 |

### 工程进阶阶段

| # | 学习主题 | 优先级 | 说明 |
|---|---------|--------|------|
| 6 | Redis | ⭐⭐ | 缓存、会话管理 |
| 7 | 消息队列 Kafka | ⭐⭐ | 异步任务、事件驱动 |
| 8 | mini-code 开发 | ⭐⭐ | 端到端小型 Agent 项目 |

### 大模型进阶（参考 dive-into-llms 补充）

| # | 学习主题 | 来源 | 说明 |
|---|---------|------|------|
| 9 | 提示学习与思维链（Prompt & CoT） | dive-into-llms ch2 | Zero-shot / Few-shot / Chain-of-Thought |
| 10 | 模型微调与部署（Fine-tuning） | dive-into-llms ch1 | Transformers 微调 + Gradio 部署 |
| 11 | 知识编辑（Knowledge Editing） | dive-into-llms ch3 | 修改模型对特定知识的记忆 |
| 12 | 数学推理（Math Reasoning） | dive-into-llms ch4 | 蒸馏 mini-R1 思路 |
| 13 | 工具学习（Tool Learning） | dive-into-llms ch7 | Function Call / Tool Use |
| 14 | Agent（智能体） | dive-into-llms ch8 | Agent 设计与实现 |
| 15 | GUI Agent | dive-into-llms ch9 | 操作界面的 Agent |
| 16 | 智能体安全 | dive-into-llms ch10 | Agent 安全风险与防护 |
| 17 | RLHF 安全对齐 | dive-into-llms ch11 | 基于 PPO 的 RLHF 实验 |

### 对比分析：原路线 vs dive-into-llms

| 维度 | 原路线（你的） | dive-into-llms 补充 |
|------|--------------|-------------------|
| 深度侧重 | Agent 开发（LangChain、ReAct、MCP） | LLM 底层原理（微调、对齐、安全） |
| 补充价值 | 你缺了提示工程、思维链、模型微调 | 这些是理解 Agent 运作原理的前提 |
| 新增建议 | 插入 Prompt/CoT + 基础微调到核心阶段 | 在 LangChain 之前先理解 Prompt 和 CoT |

---

## 学习任务管理 API

当前学习任务：`scripts/study_tasks.py`（FastAPI 搭建）

**如何使用：**
```bash
cd F:\Python\Agent开发\ai-agent-practice
uvicorn scripts.study_tasks:app --reload
# 打开 http://127.0.0.1:8000/docs
```

---

## 目录结构

```text
Agent_Develop/
  notes/         学习笔记
  configs/       配置文件练习
  scripts/       脚本练习（含 study_tasks.py）
  README.md
```
