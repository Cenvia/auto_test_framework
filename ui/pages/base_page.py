# 页面基类

# ui/pages/base_page.py
from playwright.sync_api import Page
from config.settings import Config
from utils.logger import logger
import time


class BasePage:
    """所有页面对象的基类"""

    def __init__(self, page: Page):
        self.page = page
        self.timeout = Config.TIMEOUT
        logger.info(f"初始化页面: {self.__class__.__name__}")

    def navigate(self, url: str):
        """导航到指定URL"""
        logger.info(f"导航到: {url}")
        self.page.goto(url, timeout=self.timeout)
        self.page.wait_for_load_state("domcontentloaded")

    def click(self, selector: str, **kwargs):
        """点击元素"""
        logger.debug(f"点击: {selector}")
        self.page.click(selector, **kwargs)

    def fill(self, selector: str, text: str, **kwargs):
        """填充文本"""
        logger.debug(f"填充: {selector} <- {text}")
        self.page.fill(selector, text, **kwargs)

    def get_text(self, selector: str) -> str:
        """获取文本"""
        return self.page.text_content(selector)

    def take_screenshot(self, name: str = "screenshot"):
        """截图"""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        path = Config.SCREENSHOT_DIR / f"{name}_{timestamp}.png"
        self.page.screenshot(path=str(path), full_page=True)
        logger.info(f"截图已保存: {path}")
        return str(path)

    def wait_for_element(self, selector: str, timeout: int = None):
        """等待元素出现"""
        timeout = timeout or self.timeout
        self.page.wait_for_selector(selector, state="visible", timeout=timeout)