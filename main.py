import uvicorn
from fastapi import FastAPI,Request
from fastapi.middleware.cors import CORSMiddleware
from api.proxy import router
from api.logging import init_logging, logs  # 初始化日志

# 初始化日志系统
init_logging()
# FastAPI 应用
app = FastAPI()

# CORS 中间件
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,  # 允许凭证时不能使用通配符 *
    allow_methods=["*"],
    allow_headers=["*"],
)
# 请求和响应日志记录
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logs.bind(tags=settings.FASTAPI_LOG_TAG.upper()).info(f"收到请求: {request.method} {request.url}")
    response = await call_next(request)
    logs.bind(tags=settings.FASTAPI_LOG_TAG.upper()).info(f"响应状态: {response.status_code}")
    return response
# 注册代理路由
app.include_router(router)

# 启动 FastAPI
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=30821, limit_concurrency=8)