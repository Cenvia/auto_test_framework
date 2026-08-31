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

    # 等待结果
    time.sleep(2)

    # 截图
    baidu.take_screenshot("search_result")

    # 断言：检查标题包含"百度"
    title = page.title()
    print(f"📄 页面标题: {title}")
    assert "百度" in title
    print("✅ 百度搜索测试通过！")


def test_bing_search(page: Page):
    """测试 Bing 搜索（更稳定）"""
    page.goto("https://www.bing.com")
    page.wait_for_load_state("domcontentloaded")
    time.sleep(1)

    page.fill("#sb_form_q", "pytest")
    page.click("#sb_form_go")

    page.wait_for_load_state("networkidle")
    time.sleep(2)

    title = page.title()
    print(f"📄 页面标题: {title}")
    assert "pytest" in title.lower()
    print("✅ Bing 搜索测试通过！")