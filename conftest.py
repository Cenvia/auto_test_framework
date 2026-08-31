# conftest.py
import pytest
from playwright.sync_api import sync_playwright
from api.client import ApiClient
from config.settings import Config
import os


@pytest.fixture(scope="session")
def api_client():
    """API客户端fixture"""
    return ApiClient()


@pytest.fixture(scope="function")
def page():
    """Playwright页面fixture - 增加反检测伪装"""
    with sync_playwright() as p:
        # 使用更多伪装参数
        browser = p.chromium.launch(
            headless=Config.HEADLESS,
            args=[
                '--disable-gpu',
                '--no-sandbox',
                '--disable-dev-shm-usage',
                '--disable-setuid-sandbox',
                '--disable-blink-features=AutomationControlled',  # 关键：隐藏自动化特征
                '--disable-features=IsolateOrigins,site-per-process',
                '--start-maximized'
            ]
        )

        # 创建上下文时添加更多伪装
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            locale='zh-CN',
            timezone_id='Asia/Shanghai',
            extra_http_headers={
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            }
        )

        # 重要：注入JavaScript去除webdriver特征
        page = context.new_page()
        page.add_init_script("""
            // 去除webdriver特征
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });

            // 伪装chrome
            window.chrome = {
                runtime: {}
            };

            // 修改navigator属性
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5]
            });

            Object.defineProperty(navigator, 'languages', {
                get: () => ['zh-CN', 'zh', 'en']
            });
        """)

        yield page
        context.close()
        browser.close()