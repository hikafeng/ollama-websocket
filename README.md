# Ollama WebSocket Proxy 说明文档

## 项目简介

**Ollama WebSocket Proxy** 是一个基于 WebSocket 的代理实现，用于对接 Ollama 的功能。该项目允许通过 WebSocket 连接与 Ollama 进行交互，提供高效的数据传输方式，并支持 JWT 认证以确保安全性。

## 功能特性

- **WebSocket 代理**：提供 WebSocket 连接，转发请求到后端 Ollama 服务。
- **JWT 认证**：使用 JSON Web Token（JWT）进行用户身份验证，确保安全访问。
- **流式响应**：支持 `Server-Sent Events (SSE)`，适用于流式数据传输，如 AI 生成内容。
- **环境变量管理**：使用 `.env` 文件配置后端 URL 和密钥，方便部署与维护。

---

## 环境要求

- Python 3.10 或更高版本

---

## 安装与运行

### 1. 克隆项目

首先，您需要克隆该项目的代码库：

```bash
git clone https://github.com/hikafeng/ollama-websocket.git
cd ollama-websocket
```

### 2. 生成并配置环境变量

可以使用 Python 生成一个测试令牌：

```shell
python gen_jwt.py
```

查看 user_token.txt ,其中就有生成的Token, 在 `.env` 文件中设置必要的环境变量（如果没有 `.env` 文件，可以复制 `.env.example` 并进行修改）：

```bash
cp .env.example .env
```

然后使用文本编辑器打开 `.env` 文件，修改以下内容：

```bash
JWT_SECRET_KEY=your_secret_key_here
BACKEND_URL=http://your-backend-url.com
```

- `JWT_SECRET_KEY`：用于 JWT 认证的密钥。
- `BACKEND_URL`：Ollama 后端 API 地址。

### 3. 安装依赖

请确保您的 Python 版本符合要求，并安装必要的依赖：

```bash
pip install -r requirements.txt
```

### 4. 启动代理

运行以下命令启动 WebSocket 代理：

```bash
python main.py
```

默认情况下，代理服务器将在 `http://0.0.0.0:30821` 运行。

---

## API 说明

### 1. WebSocket 连接

客户端可以通过 WebSocket 连接到代理：

```python
import websockets
import asyncio
import json

async def websocket_client():
    uri = "ws://localhost:30821/ws"
    async with websockets.connect(uri) as websocket:
        # 发送数据
        message = json.dumps({"text": "Hello, Ollama!"})
        await websocket.send(message)

        # 接收响应
        response = await websocket.recv()
        print(f"收到响应: {response}")

asyncio.run(websocket_client())
```

### 2. HTTP 代理请求

代理会将所有 HTTP 请求转发到 `BACKEND_URL`，并进行 JWT 认证：

```bash
curl -X POST "http://localhost:30821/api/chat" \
     -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"message": "你好 Ollama!"}'
```

如果 JWT 令牌无效或未提供，将返回 `401 Unauthorized` 错误。

---

## 使用说明

- 启动代理后，WebSocket 服务器将监听连接，并提供与 Ollama 交互的功能。
- 客户端可以通过 WebSocket 连接到代理，并发送请求以调用 Ollama 提供的服务。
- 代理会自动转发 HTTP 和 WebSocket 请求到 `BACKEND_URL`，并进行身份验证。

---

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

---

## 许可证

本项目的许可证信息请参考 `LICENSE` 文件。

---

## 常见问题（FAQ）

### 1. 启动时遇到 `ModuleNotFoundError`？

请确保已安装依赖：

```bash
pip install -r requirements.txt
```

### 2. 如何生成 JWT 令牌？

可以使用 Python 生成一个测试令牌：

```shell
python gen_jwt.py
```

### 3. 如何修改 WebSocket 监听端口？

修改 `main.py`：

```python
uvicorn.run(app, host="0.0.0.0", port=30821)
```

然后重新运行：

```bash
python main.py
```

---

如果您在使用过程中遇到问题或有任何建议，请随时提交 Issue 或联系项目维护者。
