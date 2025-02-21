import httpx
from fastapi import APIRouter, Request, Response, Depends
from fastapi.responses import StreamingResponse
from api.config import BACKEND_URL
from api.auth import verify_token

router = APIRouter()

@router.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"])
async def proxy(request: Request, path: str, token_data: dict = Depends(verify_token)):
    """代理请求到后端，并进行 JWT 认证"""
    target_url = f"{BACKEND_URL}/{path}"
    method = request.method
    params = dict(request.query_params)
    headers = dict(request.headers)
    
    # 删除 Host 头，避免影响代理
    headers.pop("host", None)
    
    # 读取请求体
    body = await request.body()

    # 处理 SSE（流式响应）
    if request.url.path in ["/api/chat", "/api/generate"]:
        async def event_stream():
            async with httpx.AsyncClient() as client:
                async with client.stream(method, target_url, params=params, headers=headers, data=body, timeout=None) as upstream_response:
                    async for chunk in upstream_response.aiter_bytes():
                        yield chunk
        return StreamingResponse(event_stream(), media_type="text/event-stream")
    
    # 其他普通请求
    async with httpx.AsyncClient() as client:
        upstream_response = await client.request(method, target_url, params=params, headers=headers, data=body, timeout=None)
    
    return Response(
        content=upstream_response.content,
        status_code=upstream_response.status_code,
        headers=dict(upstream_response.headers)
    )