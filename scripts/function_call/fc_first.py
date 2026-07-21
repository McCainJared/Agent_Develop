"""
==========================================================================
Function Calling 入门示例 — 你的第一个 "让 LLM 学会调用函数" 的程序
==========================================================================

【什么是 Function Calling？】
  Function Calling（函数调用）是 LLM 的一项核心能力：你告诉 LLM "我有哪些函数/工具可用"，
  LLM 不会真的去执行这些函数，而是根据用户的自然语言输入，**判断是否需要调用某个函数**，
  如果需要，它会返回**结构化的调用参数（JSON）**。

  简单来说流程是：
    用户提问 → LLM 判断需要哪个工具 → LLM 返回函数名 + 参数
    → 你的代码去真正执行函数 → 把结果再喂给 LLM → LLM 生成最终回答

【这个脚本演示了什么？】
  这是 Function Calling 的"第 0 步"：只看 LLM 会不会返回一个工具调用请求。
  后续脚本才会补全"执行函数 → 拼接结果 → 再次请求 LLM"的完整闭环。

【本脚本体现的 Function Calling 核心概念：】
  1. 工具定义（Tool Definition）   — 用 JSON Schema 描述你有什么函数
  2. 工具注册（Tool Registration） — 把 tools 列表传给 API
  3. 工具选择策略（tool_choice）   — "auto" 让 LLM 自己决定要不要调
  4. 结构化输出（Structured Output）— LLM 不再返回自然语言，而是返回函数调用 JSON
============================================================================
"""

from openai import OpenAI

# ──────────────────────────────────────────────────────────
# 初始化客户端
# ──────────────────────────────────────────────────────────
client = OpenAI(
    api_key="sk-987c3e506a2045a6bf2cf198cd9ff085",
    base_url="https://api.deepseek.com"
)

# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  核心概念 ①：工具定义（Tool Definition）                                  ║
# ║  用 JSON Schema 向 LLM 描述"我有哪些函数可以给你用"                       ║
# ║  每个工具包含：                                                          ║
# ║    - type: "function" 固定值，表示这是一个函数类型的工具                  ║
# ║    - function.name: 函数名，LLM 会返回这个名字来表示"我要调这个"          ║
# ║    - function.description: 函数的功能描述，LLM 据此判断"该不该用这个函数"  ║
# ║    - function.parameters: 入参的 JSON Schema，LLM 据此生成调用参数        ║
# ║      - type: "object" 表示参数是一个对象（大多数 API 都要求这样定义）     ║
# ║      - properties: 各个参数的名称、类型和描述                             ║
# ║      - required: 哪些参数是必填的                                         ║
# ╚══════════════════════════════════════════════════════════════════════════╝
tools = [
    {
        "type": "function",               # ← 固定写法：表示这是一个函数工具
        "function": {
            "name": "get_weather",        # ← 函数名：LLM 返回时要引用此名称
            "description": "获取指定城市的天气信息",  # ← 关键！LLM 靠这个来决定"用户问天气时我该调哪个函数"
            "parameters": {
                "type": "object",         # ← 参数整体是一个 JSON 对象
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名称，如北京、上海"  # ← LLM 据此从用户输入中提取城市名
                    }
                },
                "required": ["city"]      # ← 必填参数列表（没有这个参数，函数没法调）
            }
        }
    }
    # 💡 扩展思考：如果你有多个工具（比如 get_weather、search_web、send_email），
    #    就在这个列表里加多个元素。LLM 会根据 description 自动选择合适的工具。
]

# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  核心概念 ②：工具注册 + 工具选择策略                                      ║
# ║  - tools=tools       → 把定义好的工具列表传给 API（"注册"到本次对话）     ║
# ║  - tool_choice="auto" → LLM 自主决定：该调工具就返回 tool_calls，         ║
# ║                         不该调就正常返回文字回复                           ║
# ║                                                                          ║
# ║  tool_choice 的其他取值：                                                 ║
# ║    - "none"  → 强制不调任何工具（即使你传了 tools）                        ║
# ║    - "required" → 强制必须调一个工具                                     ║
# ║    - {"type": "function", "function": {"name": "get_weather"}}           ║
# ║      → 强制调用指定的某个工具                                             ║
# ╚══════════════════════════════════════════════════════════════════════════╝
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "user", "content": "北京今天天气怎么样？"}
    ],
    tools=tools,           # ← 核心：把工具列表传给 LLM
    tool_choice="auto"     # ← 核心：让 LLM 自主决定要不要调工具
)

# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  核心概念 ③：LLM 的返回结果 — 不再是自然语言，而是结构化的函数调用请求    ║
# ║                                                                          ║
# ║  当 LLM 判断"需要调用工具"时，message 里会出现：                           ║
# ║    - content: None（LLM 不再生成文字回复）                                 ║
# ║    - tool_calls: [                                                       ║
# ║        {                                                                 ║
# ║          "id": "call_xxx",            ← 本次调用的唯一 ID                  ║
# ║          "type": "function",                                              ║
# ║          "function": {                                                    ║
# ║            "name": "get_weather",     ← LLM 选择了哪个函数                 ║
# ║            "arguments": '{"city": "北京"}'  ← LLM 从用户输入中提取的参数  ║
# ║          }                                                               ║
# ║        }                                                                 ║
# ║      ]                                                                   ║
# ║                                                                          ║
# ║  这就是 Function Calling 最核心的魔法：                                    ║
# ║    "北京今天天气怎么样？" 这句自然语言，                                    ║
# ║    被 LLM 转化为了 get_weather(city="北京") 这个结构化的函数调用。         ║
# ║                                                                          ║
# ║  后续步骤（本脚本未演示，在后续脚本中补全）：                                ║
# ║    ① 收到 tool_calls → 你的代码执行真正的 get_weather("北京")              ║
# ║    ② 把执行结果构造成 role="tool" 的消息                                   ║
# ║    ③ 把这条消息追加到 messages 列表里                                      ║
# ║    ④ 再次调用 LLM → LLM 根据工具返回结果生成最终的自然语言回复              ║
# ╚══════════════════════════════════════════════════════════════════════════╝

# 3. 看看 LLM 返回了什么
print("=== LLM 的完整回复 ===")
print(response.choices[0].message)
