#!/usr/bin/env python3
"""
示例：游戏自动化
Example: Game automation
"""

import sys
import time
sys.path.insert(0, '..')

from desktop import DesktopController

def main():
    ctrl = DesktopController()
    
    print("=== 游戏自动化示例 ===\n")
    
    # 1. 截图识别
    print("1. 截取游戏画面...")
    ctrl.screenshot_to_file("game_screen.png")
    print("   已保存: game_screen.png")
    
    # 2. 自动任务循环示例
    print("\n2. 执行日常任务...")
    
    # 模拟游戏中的重复操作
    actions = [
        ("点击任务按钮", lambda: ctrl.click(x=500, y=300)),
        ("领取奖励", lambda: ctrl.click(x=800, y=500)),
        ("关闭弹窗", lambda: ctrl.keypress('esc')),
    ]
    
    for action_name, action in actions:
        print(f"   执行: {action_name}")
        action()
        time.sleep(1)
    
    # 3. 定时重复任务
    print("\n3. 设置定时任务 (示例: 每小时执行)...")
    # 实际使用时可以用 schedule 库
    # schedule.every().hour.do(task)
    
    print("\n=== 完成 ===")

if __name__ == "__main__":
    main()
