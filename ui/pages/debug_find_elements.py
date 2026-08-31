# debug_find_elements.py
from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    print("🌐 访问百度首页...")
    page.goto("https://www.baidu.com")
    page.wait_for_load_state("domcontentloaded")
    time.sleep(2)

    # 查找所有input元素
    print("\n🔍 查找所有input元素:")
    inputs = page.query_selector_all("input")
    for i, inp in enumerate(inputs):
        inp_id = inp.get_attribute("id")
        inp_name = inp.get_attribute("name")
        inp_class = inp.get_attribute("class")
        inp_type = inp.get_attribute("type")
        inp_placeholder = inp.get_attribute("placeholder")
        is_visible = inp.is_visible()

        print(
            f"  {i + 1}. id={inp_id}, name={inp_name}, class={inp_class}, type={inp_type}, placeholder={inp_placeholder}, visible={is_visible}")

    # 查找所有可编辑元素（包括div）
    print("\n🔍 查找所有可编辑元素:")
    editable = page.query_selector_all("[contenteditable='true'], [role='textbox']")
    for i, elem in enumerate(editable):
        elem_id = elem.get_attribute("id")
        elem_class = elem.get_attribute("class")
        elem_role = elem.get_attribute("role")
        print(f"  {i + 1}. id={elem_id}, class={elem_class}, role={elem_role}")

    # 尝试查找最可能的搜索框
    print("\n🎯 尝试常见选择器:")
    selectors = [
        "#kw",
        "input[name='wd']",
        "input[type='text']",
        ".s_ipt",
        "input#kw",
        "input[name='word']"
    ]

    for sel in selectors:
        try:
            elem = page.query_selector(sel)
            if elem:
                visible = elem.is_visible()
                print(f"  ✅ {sel} -> 存在, 可见={visible}")
                if visible:
                    # 尝试获取值
                    value = elem.get_attribute("value")
                    print(f"     当前值: '{value}'")
            else:
                print(f"  ❌ {sel} -> 不存在")
        except Exception as e:
            print(f"  ⚠️ {sel} -> 错误: {e}")

    # 截图保存
    page.screenshot(path="baidu_all_elements.png")
    print("\n📸 截图已保存: baidu_all_elements.png")

    browser.close()