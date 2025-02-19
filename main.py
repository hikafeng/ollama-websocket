#!/usr/bin/env python
# -*- coding: utf-8 -*-

import uvicorn
from fastapi import FastAPI, Request, Response
from fastapi.responses import StreamingResponse
import httpx
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
# CORS 中间件
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 请根据实际情况修改后端地址
BACKEND_URL = "http://localhost:6399"

@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"])
async def proxy(request: Request, path: str):
    # 构造完整的后端请求 URL
    target_url = f"{BACKEND_URL}/{path}"
    method = request.method
    params = dict(request.query_params)
    headers = dict(request.headers)
    # 注意：有些情况下可能需要删除 Host 头
    headers.pop("host", None)
    body = await request.body()

    # 如果是 /api/chat 接口，则返回流式的 SSE 响应
    if request.url.path == "/api/chat":
        async def event_stream():
            async with httpx.AsyncClient() as client:
                # timeout=None 防止长连接超时
                async with client.stream(method, target_url, params=params, headers=headers, data=body, timeout=None) as upstream_response:
                    async for chunk in upstream_response.aiter_bytes():
                        yield chunk
        # 这里 media_type 必须指定为 "text/event-stream"
        return StreamingResponse(event_stream(), media_type="text/event-stream")
    else:
        # 对其它接口直接转发，并将后端响应返回给客户端
        async with httpx.AsyncClient() as client:
            upstream_response = await client.request(method, target_url, params=params, headers=headers, data=body, timeout=None)
        return Response(
            content=upstream_response.content,
            status_code=upstream_response.status_code,
            headers=dict(upstream_response.headers)
        )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)