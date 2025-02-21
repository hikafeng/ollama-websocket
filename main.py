import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.proxy import router

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

# 注册代理路由
app.include_router(router)

# 启动 FastAPI
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, limit_concurrency=8)