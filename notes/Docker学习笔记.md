# Docker 学习笔记

> **一句话总结：** Docker 是一个"打包工具"，把应用和它的运行环境（依赖、配置）打包成一个**镜像**，在任何机器上以**容器**形式运行，做到"一次构建，到处运行"。

---

## 大纲

- [1. 核心概念](#1-核心概念)
- [2. 常用命令](#2-常用命令)
  - [2.1 镜像相关命令](#21-镜像相关命令)
  - [2.2 容器相关命令](#22-容器相关命令)
  - [2.3 docker ps 输出解读](#23-docker-ps-输出解读)
- [3. Dockerfile 详解](#3-dockerfile-详解)
  - [3.1 常用指令](#31-常用指令)
  - [3.2 完整示例](#32-完整示例)
- [4. 关键知识点](#4-关键知识点)
  - [4.1 CMD 为什么用 JSON 数组格式](#41-cmd-为什么用-json-数组格式)
  - [4.2 容器内 --host 为什么用 0.0.0.0](#42-容器内---host-为什么用-0000)
  - [4.3 容器里为什么需要 pip install](#43-容器里为什么需要-pip-install)
  - [4.4 docker build 的构建上下文](#44-docker-build-的构建上下文)
  - [4.5 docker run 参数拆解](#45-docker-run-参数拆解)
  - [4.6 镜像名和文件名的关系](#46-镜像名和文件名的关系)
- [5. 常见错误](#5-常见错误)
- [6. 回顾思考](#6-回顾思考)

---

## 1. 核心概念

### 必须记住

| 概念 | 一句话 | 用途 | 类比 |
|------|--------|------|------|
| **镜像（Image）** | 一个只读的模板，包含运行环境和代码 | 用来创建容器的模板，可以分发、共享 | 像 ISO 安装盘 |
| **容器（Container）** | 镜像运行后的实例，可读写 | 实际跑起来的服务，可以启动、停止、删除 | 像用安装盘装好的电脑 |
| **仓库（Registry）** | 存镜像的地方（默认 Docker Hub） | 拉取和上传镜像的中央仓库 | 像应用商店 |
| **Dockerfile** | 描述如何构建镜像的文本文件 | 自动化构建镜像，可版本控制 | 像安装说明书 |
| **端口映射** | 把容器的端口暴露到宿主机 | 让宿主机（你的电脑）能访问容器里的服务 | 给盒子开个窗户 |

### 回顾思考

> 为什么要有镜像和容器两层，直接跑不行吗？
> —— 镜像是**交付物**（你发给别人用的），容器是**运行态**（启动、停止、重启）。一个镜像可以同时启动多个容器，互不干扰。就像"安装盘"可以装到无数台电脑上。

---

## 2. 常用命令

> 整个流程：**pull（拉镜像）→ run（跑容器）→ ps（看状态）→ stop（停掉）→ rm（删除）**

### 2.1 镜像相关命令

| 命令 | 用途 | 例子 |
|------|------|------|
| `docker pull <镜像名>` | 从仓库拉取镜像到本地 | `docker pull nginx` |
| `docker images` | 查看本地所有镜像 | — |
| `docker build -t <标签> .` | 根据 Dockerfile 构建镜像 | `docker build -t my-api .` |

### 2.2 容器相关命令

| 命令 | 用途 | 例子 |
|------|------|------|
| `docker run -d -p <本机端口>:<容器端口> --name <名字> <镜像>` | 后台运行容器并映射端口 | `docker run -d -p 8080:80 --name my-nginx nginx` |
| `docker ps` | 查看运行中的容器 | — |
| `docker ps -a` | 查看所有容器（含已停止的） | — |
| `docker stop <容器名/ID>` | 停止容器 | `docker stop my-nginx` |
| `docker rm <容器名/ID>` | 删除已停止的容器 | `docker rm my-nginx` |

### 2.3 docker ps 输出解读

```
CONTAINER ID   IMAGE   COMMAND    CREATED      STATUS      PORTS                  NAMES
```

| 列 | 含义 |
|----|------|
| **CONTAINER ID** | 容器唯一标识（取前 12 位） |
| **IMAGE** | 基于哪个镜像 |
| **COMMAND** | 容器启动时执行的命令 |
| **CREATED** | 创建时间 |
| **STATUS** | 运行状态：`Up X minutes` 正常运行，`Exited (0)` 正常退出，`Exited (1)` 出错 |
| **PORTS** | 端口映射，格式 `宿主机端口->容器端口/协议` |
| **NAMES** | 容器名字（可自定义或自动生成） |

### 回顾思考

> `docker ps` 的 STATUS 为什么要看？
> —— 这是**第一件事**。容器崩了你先看 STATUS：`Up` 表示还活着，`Exited (0)` 表示正常结束，`Exited (1)` 表示出错了。Exit code 1 就说明代码/配置有问题，需要查日志。

---

## 3. Dockerfile 详解

### 3.1 常用指令

| 指令 | 用途 | 例子 |
|------|------|------|
| **FROM** | 基于哪个基础镜像（起点） | `FROM python:3.13-slim` |
| **WORKDIR** | 设置容器内的工作目录 | `WORKDIR /app` |
| **RUN** | 构建镜像时执行的命令（安装依赖等） | `RUN pip install fastapi uvicorn` |
| **COPY** | 把本机文件复制到容器里 | `COPY scripts/ /app/scripts/` |
| **CMD** | 容器启动时执行的命令（JSON 数组格式） | `CMD ["uvicorn", "scripts.study_tasks:app", "--host", "0.0.0.0"]` |

### 3.2 完整示例

```dockerfile
FROM python:3.13-slim
WORKDIR /app
RUN pip install fastapi uvicorn
COPY scripts/ /app/scripts/
CMD ["uvicorn", "scripts.study_tasks:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 回顾思考

> 为什么叫 Dockerfile 不叫别的名字？
> —— Docker 默认找的就是 `Dockerfile`（没有后缀），就像 FastAPI 默认找 `main.py`。你也可以用别的名字，但要 `docker build -f MyDockerfile .` 指定。建议就用默认名，省事。

---

## 4. 关键知识点

### 4.1 CMD 为什么用 JSON 数组格式

| 格式 | 写法 | 区别 |
|------|------|------|
| **JSON 数组格式 ✅** | `CMD ["uvicorn", "app:app"]` | Docker 直接启动进程，不经过 shell |
| **Shell 格式 ❌** | `CMD uvicorn app:app` | Docker 先启动 shell，shell 再启动进程 |

JSON 数组格式的好处：信号直接传给进程，`docker stop` 能快速停止，不会超时。

> **为什么不能经过 shell？**
> 因为 `docker stop` 发的是 Linux 信号（SIGTERM），shell 不一定转发给子进程。不转发的话 Docker 只能等超时（10 秒）后强制杀掉。

### 4.2 容器内 --host 为什么用 0.0.0.0

| 地址 | 监听范围 |
|------|---------|
| `127.0.0.1` | 只监听容器内部（localhost），容器外面访问不到 |
| `0.0.0.0` | 监听所有网络接口，包括容器外部 |

> `-p 8000:8000` 把宿主机 8000 端口接到容器 8000 端口，但容器的 uvicorn 如果只监听 `127.0.0.1`，那从宿主机发来的请求会被拒绝。所以必须写 `0.0.0.0`。

### 4.3 容器里为什么需要 pip install

Docker 容器是一个**最小化的 Linux 系统**（slim 版本只有 50MB 左右），只有 Python 解释器，**没有第三方库**。

```
本机电脑：Python + 装了几十个库 ✅
容器起跑：只有 Python，什么都没有 ❌
所以 Dockerfile 里：RUN pip install ... ✅
```

### 4.4 docker build 的构建上下文

```powershell
docker build -t study-tasks-api .
```

最后的 `.` 表示**当前目录**——Docker 引擎把整个目录打包发给 Docker 守护进程（daemon），守护进程在目录里找 Dockerfile，按指令构建。

> 注意：`.` 目录里的**所有文件**都会被发送。所以不要在大目录里 build，**只在包含 Dockerfile 的项目目录里 build**，否则文件太多 build 很慢。

### 4.5 docker run 参数拆解

```powershell
docker run -d -p 8000:8000 --name study-api study-tasks-api
```

| 参数 | 含义 |
|------|------|
| `run` | 创建并启动容器 |
| `-d` | detach，后台运行，不占用终端 |
| `-p 8000:8000` | 端口映射：宿主机 8000 → 容器 8000 |
| `--name study-api` | 给容器取名字，方便后续操作 |
| `study-tasks-api` | 用哪个镜像来创建容器 |

### 4.6 镜像名和文件名的关系

> **镜像名和 .py 文件名没有关系！**

- `-t study-tasks-api` 只是给镜像取个**标签名**
- `CMD ["uvicorn", "scripts.study_tasks:app"]` 告诉 uvicorn 找哪个**文件和变量**
- 就算 `docker build -t abc-xyz`，只要 `CMD` 里的路径正确，一样能跑

---

## 5. 常见错误

| 错误 | 原因 | 解决 |
|------|------|------|
| `port is already allocated` | 端口被占用 | 换一个端口或停掉占用端口的容器 |
| `Unable to find image locally` | 镜像不存在 | 先 `docker build` 或 `docker pull` |
| `failed to connect to docker API` | Docker Desktop 没启动 | 启动 Docker Desktop |
| `name "null" is not defined` | Python 文件里写了 `null` | Python 用 `None`，不是 `null` |

---

## 6. 回顾思考

> **Docker 解决了什么问题？**
> "我电脑上能跑"——以前这句是玩笑也是噩梦。Docker 把环境和代码打包在一起，不管在谁的电脑上、什么系统上，跑起来都一样。

> **镜像和容器有什么区别？**
> 镜像是**菜谱**，容器是**炒出来的菜**。一个菜谱可以炒无数盘菜，每盘菜（容器）独立存在，互不干扰。

> **为什么需要端口映射？**
> 容器有自己的网络空间，外面看不到容器的 `localhost`。`-p 8080:80` 就像在墙上开个洞——外面敲 8080，声音传到容器里的 80 端口。

> **为什么 CMD 要用数组格式？**
> 不用经过 shell 翻译，信号直接发给进程。否则 `docker stop` 可能要等 10 秒，因为 shell 没把信号传下去。

> **Docker 和虚拟机的区别？**
> 虚拟机虚拟一整套硬件 + 操作系统，占用大、启动慢。Docker 共用宿主机的操作系统内核，只隔离应用层，启动是毫秒级的。
