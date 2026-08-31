# config/settings.py
import os
from pathlib import Path
from dotenv import load_dotenv

# 加载.env文件
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent


class Config:
    # 从环境变量读取配置
    ENV = os.getenv("ENV", "test")
    HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
    BROWSER = os.getenv("BROWSER", "chromium")

    # API配置
    API_BASE_URL = os.getenv("API_BASE_URL", "https://jsonplaceholder.typicode.com")

    # UI配置
    UI_BASE_URL = "https://www.baidu.com"
    TIMEOUT = 30000

    # 路径配置
    BASE_DIR = BASE_DIR
    REPORT_DIR = BASE_DIR / "reports"
    SCREENSHOT_DIR = BASE_DIR / "screenshots"
    LOG_DIR = BASE_DIR / "logs"
    DATA_DIR = BASE_DIR / "data"

    # 自动创建目录
    for dir_path in [REPORT_DIR, SCREENSHOT_DIR, LOG_DIR, DATA_DIR]:
        dir_path.mkdir(exist_ok=True)