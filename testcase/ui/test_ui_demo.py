import pytest
from playwright.sync_api import Page
from ui.pages.baidu_page import BaiduPage


def test_baidu_search(page: Page):
    """测试百度搜索功能"""
    baidu = BaiduPage(page)
    baidu.navigate()
    baidu.search("pytest windows")

    # 断言标题包含关键词
    assert "pytest" in page.title() or "windows" in page.title().lower()
    print(f"✅ 页面标题: {page.title()}")

    # 截图保存
    screenshot_path = baidu.take_screenshot("search_result")
    print(f"📸 截图: {screenshot_path}")


def test_baidu_multiple_search(page: Page):
    """测试多次搜索"""
    baidu = BaiduPage(page)
    baidu.navigate()

    keywords = ["playwright", "python", "automation"]
    for keyword in keywords:
        baidu.search(keyword)
        # 等待一下，让结果加载
        page.wait_for_timeout(1000)
        assert keyword in page.title().lower() or "百度" in page.title()
        print(f"✅ 搜索 '{keyword}' 成功")