# 命令行、路径与 JSON 复盘笔记

> 这份笔记用于复习命令行、项目目录、路径、JSON 和 Tool Call 的基础知识。重点记录已经掌握的概念，以及练习中暴露出来的薄弱点。

## 大纲

- [命令行是什么](#cli-basic)
- [当前目录](#current-directory)
- [常用命令](#common-commands)
- [项目目录结构](#project-structure)
- [相对路径与绝对路径](#path-basic)
- [点和双点](#dot-dotdot)
- [运行 Python 脚本](#run-python)
- [JSON 核心知识](#json-core)
- [对象与数组](#object-array)
- [JSON 常见错误](#json-mistakes)
- [Python 读取 JSON](#python-json)
- [Function Call 和 Tool Call](#tool-call)
- [练习中出错的知识点](#wrong-points)
- [一页速查](#cheatsheet)
- [自测题](#quiz)

<a id="cli-basic"></a>

## 命令行是什么

命令行是通过输入命令来操作电脑的一种方式。以后做 AI Agent 开发时，经常需要用命令行完成这些事情：

- 切换项目目录。
- 查看文件和文件夹。
- 创建文件或文件夹。
- 运行 Python 脚本。
- 执行 Git 命令。
- 启动本地服务。

**重点：命令行不是单独学习一套无关知识，而是以后开发 Agent、运行脚本、上传 GitHub 的基础工具。**

<a id="current-directory"></a>

## 当前目录

当前目录就是命令行现在所在的文件夹。

比如当前目录是：

```text
F:\Python\Agent开发\ai-agent-practice
```

此时执行：

```powershell
dir configs
```

意思是查看：

```text
F:\Python\Agent开发\ai-agent-practice\configs
```

**重点：相对路径会从当前目录开始找。**

你已经理解：

```text
命令默认都是在当前目录下执行。
当前操作通常也是围绕当前目录展开的。
```

<a id="common-commands"></a>

## 常用命令

### `dir`

查看当前目录下的文件和文件夹。

```powershell
dir
```

查看指定文件夹：

```powershell
dir configs
```

### `cd`

切换目录。

```powershell
cd scripts
```

切换到上一级目录：

```powershell
cd ..
```

切换到绝对路径：

```powershell
cd "F:\Python\Agent开发\ai-agent-practice"
```

### `mkdir`

创建文件夹。

```powershell
mkdir notes
mkdir configs
mkdir scripts
```

### `New-Item`

PowerShell 中创建文件或文件夹的命令。

创建文件：

```powershell
New-Item notes\day1.md -ItemType File
```

创建文件夹：

```powershell
New-Item notes -ItemType Directory
```

如果 `New-Item` 不好用，也可以先用编辑器创建文件，或者用更熟悉的方式创建。

**重点：命令背后的目的比命令本身更重要。这里的目的就是创建练习用的文件和目录。**

<a id="project-structure"></a>

## 项目目录结构

当前练习项目可以按这种方式组织：

```text
ai-agent-practice/
  notes/
  configs/
  scripts/
```

含义：

- `notes/`：存放学习笔记，例如 Markdown 笔记。
- `configs/`：存放配置文件，例如 `config.json`、`config.yaml`。
- `scripts/`：存放 Python 脚本，例如 `read_config.py`。

**重点：目录名不是固定魔法，而是人为约定。好的目录结构能让项目更清楚。**

<a id="path-basic"></a>

## 相对路径与绝对路径

### 相对路径

相对路径是从当前目录出发寻找文件。

```text
configs\config.json
```

如果当前目录是：

```text
F:\Python\Agent开发\ai-agent-practice
```

那么它指向：

```text
F:\Python\Agent开发\ai-agent-practice\configs\config.json
```

### 绝对路径

绝对路径从盘符开始，可以直接定位到文件或文件夹。

```text
F:\Python\Agent开发\ai-agent-practice\configs\config.json
```

**重点：绝对路径不依赖当前目录，相对路径依赖当前目录。**

<a id="dot-dotdot"></a>

## 点和双点

在路径里：

```text
.  表示当前目录
.. 表示上一级目录
```

常见用法：

```powershell
cd ..
```

表示回到上一级目录。

```powershell
dir ..\configs
```

表示不切换目录，直接查看上一级目录中的 `configs` 文件夹。

**重点：你已经会先 `cd ..` 再 `dir configs`，接下来要熟悉直接写 `dir ..\configs`。**

<a id="run-python"></a>

## 运行 Python 脚本

如果当前目录是项目根目录：

```text
F:\Python\Agent开发\ai-agent-practice
```

运行脚本应该写：

```powershell
python scripts\read_config.py
```

不推荐写：

```powershell
run read_config.py
```

原因：`run` 不是 PowerShell 中运行 Python 文件的标准命令。

**重点：运行 Python 脚本时，要用 `python 文件路径`。**

<a id="json-core"></a>

## JSON 核心知识

JSON 是一种结构化数据格式，经常用于配置文件、API 请求和返回、结构化输出、Tool Call 参数。

基本结构：

```json
{
  "agent_name": "study-agent",
  "model": "deepseek-chat",
  "max_steps": 5,
  "enabled": true
}
```

含义：

- `"agent_name"` 是 key。
- `"study-agent"` 是 value，类型是字符串。
- `5` 是数字。
- `true` 是布尔值。

**重点：JSON 里字符串和 key 必须使用双引号。**

<a id="object-array"></a>

## 对象与数组

### 对象 `{}`

对象用来描述一个东西的多个属性。

```json
{
  "memory": {
    "enabled": true,
    "path": "./notes"
  }
}
```

这里 `memory` 的 value 是一个对象，里面有 `enabled` 和 `path` 两个配置。

### 数组 `[]`

数组用来表示一组同类内容。

```json
{
  "tools": ["read_file", "search"]
}
```

这里 `tools` 是一个数组，里面有两个字符串。

### 数组里放对象

当每个工具不仅有名字，还有启用状态时，就需要数组里放对象。

```json
{
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
}
```

**重点：数组里放字符串，只能表达一组名字；数组里放对象，可以表达一组带属性的东西。**

<a id="json-mistakes"></a>

## JSON 常见错误

### 1. 最后一个 key-value 后面多写逗号

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

### 2. 使用单引号

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

### 3. 把布尔值写成字符串

合法但含义不一样：

```json
{
  "enabled": "true"
}
```

这里 `"true"` 是字符串。

真正的布尔值：

```json
{
  "enabled": true
}
```

**重点：`"true"` 和 `true` 不是一回事。**

<a id="python-json"></a>

## Python 读取 JSON

示例：

```python
import json

with open("configs/config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

print(config["agent_name"])
print(config["memory"]["path"])
```

`config["memory"]["path"]` 的过程：

先取：

```python
config["memory"]
```

得到：

```python
{
    "enabled": True,
    "path": "./notes"
}
```

再取：

```python
["path"]
```

得到：

```text
./notes
```

**重点：这不是函数调用，而是通过 key 一层一层取 value。**

<a id="tool-call"></a>

## Function Call 和 Tool Call

Function Call 或 Tool Call 的核心是：模型用结构化参数告诉程序要调用哪个工具，以及传什么参数。

用户说：

```text
帮我读取 notes/day1.md
```

模型可能生成：

```json
{
  "tool": "read_file",
  "arguments": {
    "path": "notes/day1.md"
  }
}
```

程序看到后，真正执行读取文件的动作。

**重点：模型不是真的直接操作文件，真正执行工具的是外部程序。**

Tool Call 不只用于文件操作，也可以用于：

- 搜索网页。
- 查询 Notion。
- 查询数据库。
- 调用 API。
- 运行代码。
- 发送消息。

<a id="wrong-points"></a>

## 练习中出错的知识点

### 路径部分

**薄弱点 1：`..\configs` 这种路径写法还不够熟。**

你更习惯：

```powershell
cd ..
dir configs
```

需要继续熟悉：

```powershell
dir ..\configs
```

它表示不切换当前目录，直接查看上一级目录里的 `configs`。

### Python 运行部分

**薄弱点 2：运行 Python 文件时不要写 `run read_config.py`。**

正确：

```powershell
python scripts\read_config.py
```

### JSON 数组部分

**薄弱点 3：数组里放对象一开始不稳定。**

字符串数组：

```json
{
  "tools": ["read_file", "search"]
}
```

对象数组：

```json
{
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
}
```

判断方法：

- 如果只是一组名字，用字符串数组。
- 如果每一项有多个属性，用对象数组。

### JSON 语法部分

**薄弱点 4：要继续敏感区分字符串和布尔值。**

```json
"enabled": "true"
```

表示字符串。

```json
"enabled": true
```

表示布尔值。

### Tool Call 理解部分

**薄弱点 5：Tool Call 不是简单读取 JSON 配置里的 tools。**

更准确的理解：

```text
模型根据用户需求选择工具，并生成 JSON 格式的工具参数。
程序接收这个工具调用请求，真正执行工具。
```

<a id="cheatsheet"></a>

## 一页速查

### 命令行

```powershell
dir
cd scripts
cd ..
mkdir notes
New-Item notes\day1.md -ItemType File
python scripts\read_config.py
```

### 路径

```text
configs\config.json                 相对路径
F:\Python\Agent开发\ai-agent-practice\configs\config.json  绝对路径
.                                    当前目录
..                                   上一级目录
```

### 项目结构

```text
notes/    学习笔记
configs/  配置文件
scripts/  Python 脚本
```

### JSON

```json
{
  "agent_name": "study-agent",
  "max_steps": 5,
  "enabled": true,
  "tools": ["read_file", "search"],
  "memory": {
    "path": "./notes"
  }
}
```

### Python 读取 JSON

```python
import json

with open("configs/config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

print(config["memory"]["path"])
```

### GitHub 上传常用命令

```powershell
git status
git add README.md notes\Markdown学习记录.md
git commit -m "docs: add notes"
git push
```

<a id="quiz"></a>

## 自测题

- [ ] `configs\config.json` 是相对路径还是绝对路径？为什么？
- [ ] `cd ..` 和 `dir ..\configs` 有什么区别？
- [ ] 当前目录为什么会影响 Python 读取文件？
- [ ] JSON 中 `{}` 和 `[]` 分别适合表达什么？
- [ ] 为什么 JSON 里 key 必须用双引号？
- [ ] `"enabled": "true"` 和 `"enabled": true` 有什么区别？
- [ ] `config["memory"]["path"]` 是怎么一步一步取到 `./notes` 的？
- [ ] Tool Call 中，模型负责什么？程序负责什么？
