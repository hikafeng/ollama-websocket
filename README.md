# Ollama WebSocket Proxy 说明文档

## 项目简介
**Ollama WebSocket Proxy** 是一个基于 WebSocket 的代理实现，用于对接 Ollama 的功能。该项目允许通过 WebSocket 连接与 Ollama 进行交互，提供高效的数据传输方式。

## 环境要求
- Python 3.10 或更高版本

## 安装与运行

### 1. 克隆项目
首先，您需要克隆该项目的代码库：
```bash
git clone https://github.com/hikafeng/ollama-websocket.git
cd ollama-websocket
```

### 2. 安装依赖
请确保您的 Python 版本符合要求，并安装必要的依赖（如果有的话）：
```bash
pip install -r requirements.txt
```

### 3. 启动代理
运行以下命令启动 WebSocket 代理：
```bash
python proxy.py
```

## 使用说明
- 启动代理后，WebSocket 服务器将开始监听连接，并提供与 Ollama 交互的功能。
- 客户端可以通过 WebSocket 连接到该代理，并发送请求以调用 Ollama 提供的服务。

## 贡献指南
如果您希望为本项目做出贡献，可以按照以下步骤进行：
1. Fork 该项目到您的 GitHub 账户。
2. 创建一个新的分支进行开发：
   ```bash
   git checkout -b feature-branch
   ```
3. 提交您的修改：
   ```bash
   git commit -am "添加新功能"
   ```
4. 推送到您的远程仓库：
   ```bash
   git push origin feature-branch
   ```
5. 在 GitHub 上提交 Pull Request，等待审核合并。

## 许可证
本项目的许可证信息请参考 `LICENSE` 文件。

---

如果您在使用过程中遇到问题或有任何建议，请随时提交 Issue 或联系项目维护者。