import os
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()

# 读取配置
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
BACKEND_URL = os.getenv("BACKEND_URL")
ALGORITHM = os.getenv("ALGORITHM")
USER_INFO = os.getenv("USER_INFO", "user,admin")
USER_INFO_LIST = [{"user": u.strip()} for u in USER_INFO.split(',')]
# 确保环境变量已正确加载
if not SECRET_KEY or not BACKEND_URL:
    raise ValueError("请在 .env 文件中设置 JWT_SECRET_KEY 和 BACKEND_URL")

from configparser import ConfigParser

class Settings:
    def __init__(self):
        _parser = ConfigParser()
        _parser.read("config.ini")

        # 读取全局配置
        if _parser.has_section("global"):
            _global_section = _parser["global"]
        else:
            _global_section = dict()

        self.TITLE = _global_section.get("title", "")
        self.PORT = int(_global_section.get("port", "3000"))
        self.OPEN_DOCS = _global_section.get("open_docs", "False").lower() == "true"
        self.API_VERSION = _global_section.get("api_version", "0.0.1")
        self.LIMIT_CONCURRENCY = int(_global_section.get("limit_concurrency", "100"))

        # 读取日志相关配置
        if _parser.has_section("logging_set"):
            _logging_set_section = _parser["logging_set"]
        else:
            _logging_set_section = dict()

        # 日志SET项
        self.LOG_ROTATION = _logging_set_section.get("log_rotation", "10 MB")
        self.LOG_RETENTION = _logging_set_section.get("log_retention", "10 days")
        self.LOG_COMPRESSION = _logging_set_section.get("log_compression", "zip")
        self.LOG_LEVEL = _logging_set_section.get("log_level", "INFO")
        self.LOG_BACKTRACE = _logging_set_section.get("log_backtrace", "True").lower() == "true"
        self.LOG_DIAGNOSE = _logging_set_section.get("log_diagnose", "True").lower() == "true"
        self.LOG_SET_DEFAULT_TAG = _logging_set_section.get("log_set_default_tag", "custom")
        
        # 日志GET项
        if _parser.has_section("logging_get"):
            _logging_get_section = _parser["logging_get"]
        else:
            _logging_get_section = dict()

        self.LOG_USER = _logging_get_section.get("user", "cloudwise")
        self.LOG_GET_DEFAULT_TAG = _logging_get_section.get("log_get_default_tag", "all")
        self.ALLOWED_TAGS = _logging_get_section.get("allowed_tags", "fastapi,custom").split(",")
        self.DEFAULT_ROWS = int(_logging_get_section.get("default_rows", "100"))
        self.MAX_ROWS = int(_logging_get_section.get("max_rows", "1000"))
        self.LOG_FILE_PATH = _logging_get_section.get("log_file_path", "logs/app.log")
        
        # Fastapi自身日志
        if _parser.has_section("logging_fastapi"):
            _logging_fastapi_section = _parser["logging_fastapi"]
        else:
            _logging_fastapi_section = dict()
        self.FASTAPI_LOG_TAG = _logging_fastapi_section.get("fastapi_log_tag", "FASTAPI")
        self.UVICORN_LOG_FILE = _logging_fastapi_section.get("uvicorn_log_file", "/logs/uvicorn_logs.log")
        self.UVICORN_LOG_LEVEL= _logging_fastapi_section.get("log_level", "INFO").upper()
        self.UVICORN_LOG_FORMAT = _parser.get('logging_fastapi', 'log_format', fallback='%(asctime)s | %(levelname)s | %(message)s')
        self.UVICORN_LOG_MAX_FILE_SIZE= int(_logging_fastapi_section.get("max_log_file_size", "10485760"))
        self.UVICORN_LOG_BACKUP_COUNT = int(_logging_fastapi_section.get("backup_count", "5"))

# 实例化配置
settings = Settings()