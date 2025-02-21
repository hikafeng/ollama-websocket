import os
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()

# 读取配置
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
BACKEND_URL = os.getenv("BACKEND_URL")
ALGORITHM = "HS256"

# 确保环境变量已正确加载
if not SECRET_KEY or not BACKEND_URL:
    raise ValueError("请在 .env 文件中设置 JWT_SECRET_KEY 和 BACKEND_URL")