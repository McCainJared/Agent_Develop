# Markdown、YAML 与 GitHub 上传复盘笔记

> 这份笔记用于复习 YAML、Markdown、README 和 GitHub 上传流程。重点记录已经掌握的知识，以及练习中暴露出来的薄弱点。

## 大纲

- [YAML 核心知识](#yaml-core)
- [YAML 容易出错的点](#yaml-mistakes)
- [YAML 与 JSON 的关系](#yaml-json)
- [Markdown 核心知识](#markdown-core)
- [任务清单](#task-list)
- [Markdown 表格](#markdown-table)
- [README 是什么](#readme)
- [GitHub 上传流程](#github-flow)
- [练习中出错的知识点](#wrong-points)
- [一页速查](#cheatsheet)
- [自测题](#quiz)

<a id="yaml-core"></a>

## YAML 核心知识

YAML 是一种适合人类阅读和修改的配置文件格式，经常用来写项目配置、Agent 配置、工作流配置等。

**重点：YAML 用缩进表示层级。**

```yaml
agent:
  name: study-agent
  model: deepseek-chat
  max_steps: 5
```

含义：

- `agent` 是一个对象。
- `name`、`model`、`max_steps` 都属于 `agent`。
- 缩进表示它们是 `agent` 下面的配置。

**重点：YAML 的 key 和 value 之间要有空格。**

正确：

```yaml
name: study-agent
```

不推荐或容易出错：

```yaml
name:study-agent
```

<a id="yaml-mistakes"></a>

## YAML 容易出错的点

### 1. 缩进错误

错误示例：

```yaml
memory:
enabled: true
path: ./notes
```

问题：`enabled` 和 `path` 没有缩进，看不出它们是否属于 `memory`。

正确示例：

```yaml
memory:
  enabled: true
  path: ./notes
```

**重点：同一层级的缩进必须对齐。**

### 2. 列表符号 `-` 容易漏

字符串列表：

```yaml
tools:
  - read_file
  - search
```

含义：`tools` 是一个列表，里面有两个字符串。

### 3. 对象列表容易和普通列表混淆

对象列表：

```yaml
tools:
  - name: read_file
    enabled: true
  - name: search
    enabled: false
```

含义：`tools` 是一个列表，列表里每一项都是一个对象。

**重点：看到 `- name: xxx`，通常表示列表里放的是对象。**

<a id="yaml-json"></a>

## YAML 与 JSON 的关系

YAML 更适合人类读写，JSON 更适合程序稳定解析、API 传输和结构化输出。

YAML：

```yaml
memory:
  enabled: true
  path: ./notes
```

等价 JSON：

```json
{
  "memory": {
    "enabled": true,
    "path": "./notes"
  }
}
```

对象列表的 YAML：

```yaml
tools:
  - name: read_file
    enabled: true
  - name: search
    enabled: false
```

等价 JSON：

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

**重点：YAML 的缩进层级，转换成 JSON 后通常就是 `{}` 对象和 `[]` 数组的嵌套。**

<a id="markdown-core"></a>

## Markdown 核心知识

Markdown 是一种轻量级标记语言，适合写学习笔记、README、项目文档和 GitHub 说明。

常用语法：

```markdown
# 一级标题

## 二级标题

- 无序列表
- 第二项

1. 有序列表
2. 第二步

`inline code`

```python
print("hello agent")
```
```

**重点：标题的 `#` 后面要加空格。**

正确：

```markdown
# 标题
```

不推荐：

```markdown
#标题
```

<a id="task-list"></a>

## 任务清单

任务清单用于记录任务是否完成。

```markdown
- [x] 命令行
- [x] JSON
- [ ] Markdown
```

含义：

- `[x]` 表示已完成。
- `[ ]` 表示未完成。
- `- [x] 内容` 中间的空格不能乱省。

**重点：任务清单固定格式是 `- [ ] 任务` 或 `- [x] 任务`。**

常见错误：

```markdown
-[ ] 少了空格
-[] 少了中括号里的空格
- [ x ] x 两边多了空格
```

正确：

```markdown
- [ ] 未完成任务
- [x] 已完成任务
```

<a id="markdown-table"></a>

## Markdown 表格

Markdown 表格由三部分组成：表头、分隔行、数据行。

```markdown
| 阶段 | 内容 | 状态 |
| --- | --- | --- |
| 当前 | Markdown | 学习中 |
```

对应理解：

```text
阶段    内容       状态
当前    Markdown   学习中
```

**重点：表格必须有分隔行 `| --- | --- | --- |`。**

写表格时可以记住：

```text
第一行：列名
第二行：--- 分隔
第三行：具体数据
```

<a id="readme"></a>

## README 是什么

README 是 GitHub 仓库首页默认展示的说明文件，通常用来说明：

- 这个项目是什么。
- 项目里有什么内容。
- 如何使用这个项目。
- 当前学习或开发进度。
- 笔记、代码、项目分别放在哪里。

适合当前仓库的 README 结构：

```markdown
# AI Agent 从 0 到 1 学习流程

这是我的 AI Agent 开发学习仓库，用来记录基础知识、学习笔记和后续项目。

## 当前进度

| 阶段 | 内容 | 状态 |
| --- | --- | --- |
| 基础 | 命令行 / JSON / YAML / Markdown | 学习中 |

## 学习笔记

- `notes/命令行与JSON学习复盘.md`
- `notes/Markdown学习记录.md`

## 任务清单

- [x] 学习命令行
- [x] 学习 JSON
- [x] 学习 YAML
- [ ] 熟练使用 Markdown
```

**重点：README 不是随便写一段介绍，而是仓库的入口说明书。**

<a id="github-flow"></a>

## GitHub 上传流程

把修改上传到 GitHub，一般分四步：

```powershell
git status
git add README.md notes\Markdown学习记录.md
git commit -m "docs: add markdown notes"
git push
```

每一步含义：

- `git status`：查看当前有哪些文件被修改。
- `git add 文件1 文件2`：把要保存的文件加入待提交区。
- `git commit -m "说明"`：在本地生成一次提交记录。
- `git push`：把本地提交上传到 GitHub。

**重点：`git add` 后面多个文件之间用空格，不用 `/`。**

正确：

```powershell
git add README.md notes\Markdown学习记录.md
```

错误：

```powershell
git add README.md / notes\Markdown学习记录.md
```

**重点：`git commit` 要带 `-m`。**

正确：

```powershell
git commit -m "docs: add markdown notes"
```

错误：

```powershell
git commit "docs: add markdown notes"
```

<a id="wrong-points"></a>

## 练习中出错的知识点

### YAML 部分

**薄弱点 1：YAML 对象列表转换成 JSON 时容易写乱。**

正确思路：

- `tools:` 是 key。
- `- name: read_file` 表示列表中的一个对象。
- 多个 `- name:` 表示列表里有多个对象。

正确 JSON：

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

**薄弱点 2：需要继续判断列表项是字符串还是对象。**

字符串列表：

```yaml
tools:
  - read_file
  - search
```

对象列表：

```yaml
tools:
  - name: read_file
    enabled: true
  - name: search
    enabled: false
```

判断方法：

- `- read_file`：列表项是字符串。
- `- name: read_file`：列表项是对象，因为里面有 key/value。

### Markdown 部分

**薄弱点 1：任务清单格式一开始不熟。**

正确格式：

```markdown
- [x] 已完成
- [ ] 未完成
```

### 表格部分

**薄弱点 2：Markdown 表格一开始不会搭结构。**

记住模板：

```markdown
| 列1 | 列2 | 列3 |
| --- | --- | --- |
| 内容1 | 内容2 | 内容3 |
```

### Git 部分

**薄弱点 3：`git add` 多文件时误用了 `/`。**

错误：

```powershell
git add README.md / notes\Markdown学习记录.md
```

正确：

```powershell
git add README.md notes\Markdown学习记录.md
```

### Commit 部分

**薄弱点 4：`git commit` 少了 `-m`，提交说明格式也需要固定。**

错误：

```powershell
git commit "docs : add markdown notes"
```

正确：

```powershell
git commit -m "docs: add markdown notes"
```

注意：

- `commit` 后面要写 `-m`。
- `docs:` 中间不要加空格。
- 命令行里尽量使用英文半角引号 `"`。

### 文件名部分

**薄弱点 5：`README.md` 容易拼错。**

错误：

```powershell
git add READM.md
```

正确：

```powershell
git add README.md
```

<a id="cheatsheet"></a>

## 一页速查

### YAML

```yaml
agent:
  name: study-agent
  model: deepseek-chat

tools:
  - name: read_file
    enabled: true
  - name: search
    enabled: false
```

记忆点：

- 缩进表示层级。
- `key: value` 冒号后要有空格。
- `-` 表示列表。
- `- name: xxx` 通常表示列表中的对象。

### Markdown

```markdown
# 一级标题

## 二级标题

- 列表项

- [x] 已完成
- [ ] 未完成

| 列1 | 列2 |
| --- | --- |
| 内容1 | 内容2 |
```

记忆点：

- `#` 后面加空格。
- 代码用反引号。
- 表格必须有分隔行。
- 任务清单中 `[ ]` 里面有一个空格。

### README

README 是仓库首页说明书，建议包含：

- 项目是什么。
- 当前进度。
- 笔记目录。
- 任务清单。
- 后续项目或代码说明。

### Git 上传

```powershell
git status
git add README.md notes\Markdown学习记录.md
git commit -m "docs: add markdown notes"
git push
```

记忆点：

- `add` 是选择文件。
- `commit` 是本地保存记录。
- `push` 是上传到 GitHub。

<a id="quiz"></a>

## 自测题

- [ ] `tools: - read_file - search` 转成 JSON 后，`tools` 的 value 应该是什么类型？
- [ ] `tools: - name: read_file enabled: true` 为什么是对象列表？
- [ ] Markdown 任务清单里，未完成任务怎么写？
- [ ] Markdown 表格为什么必须写 `| --- | --- |` 这一行？
- [ ] `git add README.md / notes\Markdown学习记录.md` 为什么不对？
- [ ] `git commit -m "docs: add markdown notes"` 中 `-m` 的作用是什么？
- [ ] README 和普通学习笔记有什么区别？
