# ui/pages/baidu_page.py
from playwright.sync_api import Page
from config.settings import Config
import time


class BaiduPage:
    def __init__(self, page: Page):
        self.page = page
        self.page.set_default_timeout(60000)

    def navigate(self):
        """导航到百度首页"""
        print("🌐 正在访问百度首页...")
        self.page.goto("https://www.baidu.com", timeout=60000)
        self.page.wait_for_load_state("domcontentloaded", timeout=30000)
        # 等待页面稳定
        self.page.wait_for_timeout(2000)
        print("✅ 百度首页加载完成")

    def search(self, keyword: str):
        """执行搜索 - 使用JavaScript强制操作"""
        print(f"🔍 正在搜索: {keyword}")

        # 使用JavaScript直接操作DOM（最可靠的方法）
        result = self.page.evaluate(f"""
            (function() {{
                // 1. 找到输入框（即使隐藏）
                var input = document.querySelector('#kw') || 
                           document.querySelector('input[name="wd"]') ||
                           document.querySelector('.s_ipt');

                if (!input) {{
                    return '未找到输入框';
                }}

                // 2. 强制显示并设置值
                input.style.display = 'block';
                input.style.visibility = 'visible';
                input.value = '{keyword}';

                // 3. 触发事件，让页面感知到输入
                input.dispatchEvent(new Event('input', {{ bubbles: true }}));
                input.dispatchEvent(new Event('change', {{ bubbles: true }}));

                // 4. 聚焦输入框
                input.focus();

                // 5. 查找并点击搜索按钮
                var button = document.querySelector('button#chat-submit-button') ||
                            document.querySelector('#su') ||
                            document.querySelector('input[type="submit"]') ||
                            document.querySelector('button');

                if (button) {{
                    button.click();
                    return '点击按钮搜索成功';
                }} else {{
                    // 如果找不到按钮，模拟回车
                    var enterEvent = new KeyboardEvent('keydown', {{
                        key: 'Enter',
                        code: 'Enter',
                        keyCode: 13,
                        which: 13,
                        bubbles: true
                    }});
                    input.dispatchEvent(enterEvent);
                    return '按回车搜索成功';
                }}
            }})()
        """)

        print(f"   ℹ️ {result}")

        # 等待搜索结果加载
        self.page.wait_for_load_state("networkidle", timeout=30000)
        self.page.wait_for_timeout(2000)
        print("✅ 搜索完成")

    def get_title(self):
        """获取页面标题"""
        return self.page.title()

    def take_screenshot(self, name="screenshot"):
        """截图功能"""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        path = Config.SCREENSHOT_DIR / f"{name}_{timestamp}.png"
        self.page.screenshot(path=str(path), full_page=True)
        print(f"📸 截图已保存: {path}")
        return str(path)