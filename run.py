# run.py
# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
统一测试运行入口
用法:
    python run.py              # 运行所有测试
    python run.py --api        # 只运行API测试
    python run.py --ui         # 只运行UI测试
    python run.py --smoke      # 运行冒烟测试
    python run.py --report     # 生成报告
"""
import sys
import argparse
import subprocess
from pathlib import Path


def run_tests(marker: str = None, report: bool = True):
    """运行测试"""
    cmd = ["pytest", "-v"]

    if marker:
        cmd.extend(["-m", marker])

    if report:
        cmd.extend(["--html=reports/report.html", "--self-contained-html"])

    print(f"🔧 运行命令: {' '.join(cmd)}")
    return subprocess.run(cmd)


def main():
    parser = argparse.ArgumentParser(description="测试运行器")
    parser.add_argument("--api", action="store_true", help="运行API测试")
    parser.add_argument("--ui", action="store_true", help="运行UI测试")
    parser.add_argument("--smoke", action="store_true", help="运行冒烟测试")
    parser.add_argument("--report", action="store_true", help="生成HTML报告")
    parser.add_argument("--debug", action="store_true", help="调试模式")

    args = parser.parse_args()

    if args.debug:
        # 调试模式
        cmd = ["pytest", "-v", "-s", "--tb=short"]
        subprocess.run(cmd)
        return

    if args.api:
        run_tests("api", args.report)
    elif args.ui:
        run_tests("ui", args.report)
    elif args.smoke:
        run_tests("smoke", args.report)
    else:
        # 运行所有测试
        run_tests(report=args.report)


if __name__ == "__main__":
    main()