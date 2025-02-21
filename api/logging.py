from loguru import logger  # loguru 仍然使用 logger，但我们会将它绑定到 logs
from pathlib import Path
from api.config import settings  # 从配置文件中读取设置

# 日志文件目录
LOG_DIR = Path(settings.LOG_FILE_PATH).parent
LOG_DIR.mkdir(exist_ok=True)

# 配置日志记录器，绑定默认标签 "custom"
logs = logger.bind(tags=settings.LOG_SET_DEFAULT_TAG.upper())  # 使用 logs 作为新的日志对象

# 设置日志记录格式
logs.add(
    settings.LOG_FILE_PATH,  # 日志文件路径
    format="{time:YYYY-MM-DD HH:mm:ss}  | {extra[tags]:^10} | {level} | {message}",  # 精简时间格式，控制 tags 长度
    rotation=settings.LOG_ROTATION,  # 日志文件大小轮转配置
    retention=settings.LOG_RETENTION,  # 日志保留时间
    compression=settings.LOG_COMPRESSION,  # 日志文件压缩方式
    level=settings.LOG_LEVEL,  # 日志级别
    backtrace=settings.LOG_BACKTRACE,  # 捕获回溯错误
    diagnose=settings.LOG_DIAGNOSE  # 捕获详细的错误信息
)

INIT_TAGS="describe"

# 将日志记录器注册到全局
def init_logging():
    logs.bind(tags=INIT_TAGS.upper()).info(f"{'-'*14} 日志系统初始化完成 {'-'*14}")
    logs.bind(tags=INIT_TAGS.upper()).info(f"{'-'*46}")
    logs.bind(tags=INIT_TAGS.upper()).info(f"{' '*14}海内存知己，天涯若比邻。")
    logs.bind(tags=INIT_TAGS.upper()).info(f"{'-'*46}")
    
# init_logging()