# testcases/ui/test_ui_demo.py
import pytest
from playwright.sync_api import Page
from ui.pages.baidu_page import BaiduPage
import time


def test_baidu_search(page: Page):
    """测试百度搜索"""
    baidu = BaiduPage(page)
    baidu.navigate()
    baidu.search("pytest")

    time.sleep(2)
    title = page.title()
    print(f"📄 页面标题: {title}")
    assert "百度" in title
    print("✅ 百度搜索测试通过！")

