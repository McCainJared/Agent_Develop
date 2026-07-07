# 命令行与 JSON 学习复盘

学习时间：第 1 次、第 2 次  
学习主题：命令行 / 路径 / 项目结构 / JSON 基础 / Python 读取 JSON

## 一、复习大纲

1. 命令行基础
   - `cd`：切换目录
   - `dir`：查看目录内容
   - `mkdir`：创建文件夹
   - `New-Item` / `Out-File`：创建文件
   - `cd ..`：回到上一层目录

2. 路径基础
   - 当前目录
   - 相对路径
   - 绝对路径
   - `.` 和 `..`
   - Windows 路径分隔符 `\`

3. 项目目录结构
   - `notes/`：存放学习笔记
   - `configs/`：存放配置文件
   - `scripts/`：存放 Python 脚本

4. JSON 基础
   - key / value
   - 字符串、数字、布尔值
   - 对象 `{}`
   - 数组 `[]`
   - 嵌套对象
   - 数组里放对象

5. JSON 在 AI Agent 中的用途
   - 保存配置
   - API 请求与返回
   - Function Call / Tool Call 参数
   - 结构化输出

## 二、第 1 次学习：命令行与路径

### 1. 已掌握内容

**重点：当前目录会影响所有相对路径。**

你已经理解：

```text
当前目录 = 命令行现在所在的文件夹。
相对路径会从当前目录开始找。
```

例如当前目录是：

```text
F:\Python\Agent开发\ai-agent-practice
```

那么：

```powershell
dir configs
```

表示查看：

```text
F:\Python\Agent开发\ai-agent-practice\configs
```

你已经掌握的命令：

```powershell
cd ai-agent-practice
mkdir notes
mkdir configs
mkdir scripts
dir
cd scripts
cd ..
python scripts\read_config.py
```

### 2. 重要概念

**相对路径**：从当前目录出发寻找文件。

```text
configs\config.json
```

如果当前目录是项目根目录，它表示：

```text
当前目录\configs\config.json
```

**绝对路径**：从盘符开始，可以直接定位到文件或文件夹。

```text
F:\Python\Agent开发\ai-agent-practice\configs\config.json
```

**`.` 表示当前目录，`..` 表示上一层目录。**

```powershell
cd ..
dir ..\configs
```

### 3. 还不熟的地方

**需要重点复习：路径里直接使用 `..`。**

你现在能想到：

```powershell
cd ..
dir configs
```

但还不熟：

```powershell
dir ..\configs
```

它的意思是：不切换当前目录，直接查看上一层目录里的 `configs` 文件夹。

建议练习 3 遍：

```powershell
cd scripts
dir ..\configs
cd ..
cd scripts
dir ..\notes
```

### 4. 第 1 次结论

当前水平：**L2+，接近 L3**。

你已经能完成基本命令行操作，但还需要继续强化：

- `..\configs` 这种路径写法
- 当前目录对 Python 读取文件路径的影响
- 运行脚本时，应该站在项目根目录还是脚本目录

## 三、第 2 次学习：JSON

### 1. 已掌握内容

你已经理解 JSON 的基本结构：

```json
{
  "agent_name": "study-agent",
  "model": "deepseek-chat",
  "max_steps": 5,
  "enabled": true
}
```

其中：

```text
"agent_name" 是 key
"study-agent" 是 value，类型是字符串
5 是数字
true 是布尔值
```

**重点：JSON 不是 Python 字典，JSON 必须使用双引号。**

错误写法：

```json
{
  'agent_name': 'study-agent'
}
```

正确写法：

```json
{
  "agent_name": "study-agent"
}
```

### 2. 对象和数组

**对象 `{}` 用来表示一个东西的多个属性。**

```json
"memory": {
  "enabled": true,
  "path": "./notes"
}
```

这里表示：`memory` 下面有两个属性：

```text
enabled：是否启用
path：路径
```

**数组 `[]` 用来表示一组同类东西。**

```json
"tools": ["read_file", "search"]
```

这里表示：工具列表中有两个工具。

### 3. 数组里放对象

这是你需要继续强化的重点。

简单工具列表：

```json
"tools": ["read_file", "search"]
```

只能表达有哪些工具。

详细工具列表：

```json
"tools": [
  {
    "name": "read_file",
    "enabled": true
  },
  {
    "name": "search",
    "enabled": false
  }
]
```

它可以表达：

```text
read_file 工具已启用
search 工具未启用
```

**重点：数组里放字符串，只能表达一组名字；数组里放对象，可以表达一组带属性的东西。**

### 4. 常见错误

#### 错误 1：最后一个 key-value 后面加逗号

错误：

```json
{
  "agent_name": "study-agent",
  "max_steps": 5,
}
```

正确：

```json
{
  "agent_name": "study-agent",
  "max_steps": 5
}
```

#### 错误 2：用单引号

错误：

```json
{
  'model': 'deepseek-chat'
}
```

正确：

```json
{
  "model": "deepseek-chat"
}
```

#### 错误 3：把布尔值写成字符串

```json
{
  "enabled": "true"
}
```

这虽然合法，但 `"true"` 是字符串，不是真正的布尔值。

真正的布尔值应该写：

```json
{
  "enabled": true
}
```

### 5. Python 读取 JSON

```python
import json

with open("configs/config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

print(config["agent_name"])
print(config["memory"]["path"])
```

**重点：`config["memory"]["path"]` 不是调用函数，而是通过 key 取 value。**

过程是：

```python
config["memory"]
```

先取到：

```python
{
    "enabled": True,
    "path": "./notes"
}
```

再通过：

```python
["path"]
```

取到：

```text
./notes
```

### 6. JSON 在 AI Agent 中的用途

**JSON 适合在程序之间传递结构化数据。**

常见用途：

1. 保存 Agent 配置

```json
{
  "model": "deepseek-chat",
  "max_steps": 5
}
```

2. API 请求与返回

LLM API、搜索 API、天气 API 常用 JSON 传参数和返回结果。

3. Function Call / Tool Call 参数

```json
{
  "tool": "read_file",
  "arguments": {
    "path": "notes/day1.md"
  }
}
```

4. 结构化输出

```json
{
  "summary": "今天学习了 JSON",
  "next_action": "学习 YAML"
}
```

## 四、Function Call / Tool Call 理解

### 1. 核心定义

**Function Call / Tool Call = 模型用 JSON 告诉程序：我要调用哪个工具，以及传什么参数。**

模型本身不会真的读文件、写文件、查数据库。

它负责：

```text
决定用哪个工具
生成工具调用参数
```

程序负责：

```text
真正执行工具
把结果返回给模型
```

### 2. 例子

用户说：

```text
帮我读取 notes/day1.md
```

模型生成工具调用：

```json
{
  "tool": "read_file",
  "arguments": {
    "path": "notes/day1.md"
  }
}
```

程序看到后执行：

```text
read_file("notes/day1.md")
```

### 3. 需要记住

**Tool Call 不只是文件操作。**

它也可以用于：

- 查天气
- 查数据库
- 搜索网页
- 查询 Notion
- 发送邮件
- 运行代码
- 调用业务系统接口

## 五、当前薄弱点清单

### 1. 路径中的 `..` 还不熟

需要继续练：

```powershell
dir ..\configs
python ..\scripts\read_config.py
```

### 2. 数组里放对象还需要强化

重点比较：

```json
"tools": ["read_file", "search"]
```

和：

```json
"tools": [
  {"name": "read_file", "enabled": true},
  {"name": "search", "enabled": false}
]
```

### 3. Tool Call 的边界还要继续理解

现在要记住：

```text
模型只生成调用请求，真正执行工具的是程序。
```

### 4. 布尔值和字符串要保持敏感

```json
"enabled": "true"
```

和：

```json
"enabled": true
```

不是一回事。

## 六、自测题

1. `configs\config.json` 是相对路径还是绝对路径？为什么？
2. `cd ..` 和 `dir ..\configs` 有什么区别？
3. JSON 中 `{}` 和 `[]` 分别适合表达什么？
4. 为什么 JSON 里不能用单引号？
5. `"enabled": "true"` 和 `"enabled": true` 有什么区别？
6. `config["memory"]["path"]` 是怎么一步一步取到 `./notes` 的？
7. Tool Call 中，模型负责什么？程序负责什么？

## 七、下一步

下一次进入 YAML 学习。

学习目标：

```text
理解 YAML 是更适合人类阅读的配置格式，重点掌握缩进、列表、键值对和嵌套结构。
```
