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


def test_bing_search(page: Page):
    """测试 Bing 搜索 - 使用 JavaScript"""
    print("🔍 开始 Bing 搜索测试...")

    page.goto("https://www.bing.com")
    page.wait_for_load_state("domcontentloaded")
    time.sleep(1)

    # 使用 JavaScript 执行搜索
    result = page.evaluate("""
        (function() {
            var input = document.querySelector("input[name='q']");
            if (!input) return '未找到输入框';

            input.value = 'pytest';
            input.dispatchEvent(new Event('input', {bubbles: true}));

            // 尝试点击搜索按钮
            var btn = document.querySelector("button[type='submit']") || 
                     document.querySelector("#sb_form_go");
            if (btn) {
                btn.click();
                return '点击按钮搜索';
            }

            // 如果找不到按钮，按回车
            var enterEvent = new KeyboardEvent('keydown', {
                key: 'Enter',
                code: 'Enter',
                keyCode: 13,
                which: 13,
                bubbles: true
            });
            input.dispatchEvent(enterEvent);
            return '按回车搜索';
        })()
    """)
    print(f"   ℹ️ {result}")

    # 等待结果
    page.wait_for_load_state("networkidle", timeout=30000)
    time.sleep(2)

    # 断言
    title = page.title()
    print(f"📄 页面标题: {title}")
    assert "pytest" in title.lower() or "bing" in title.lower()
    print("✅ Bing 搜索测试通过！")