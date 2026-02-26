#!/usr/bin/env python3
"""
示例：自动化浏览器操作
Example: Automate browser operations
"""

import sys
import time
sys.path.insert(0, '..')

from desktop import DesktopController

def main():
    ctrl = DesktopController()
    
    print("=== 浏览器自动化示例 ===\n")
    
    # 1. 获取屏幕信息
    print("1. 获取屏幕尺寸...")
    size = ctrl.screen_size()
    print(f"   屏幕: {size['width']}x{size['height']}")
    
    # 2. 截图保存
    print("\n2. 截图保存...")
    ctrl.screenshot_to_file("browser_start.png")
    print("   已保存: browser_start.png")
    
    # 3. 使用快捷键切换标签页
    print("\n3. 切换到第2个标签页 (Ctrl+2)...")
    ctrl.hotkey('ctrl', '2')
    time.sleep(1)
    
    # 4. 滚动页面
    print("\n4. 向下滚动3次...")
    ctrl.scroll(-3)
    time.sleep(0.5)
    
    # 5. 截图对比
    print("\n5. 截图保存...")
    ctrl.screenshot_to_file("after_scroll.png")
    print("   已保存: after_scroll.png")
    
    print("\n=== 完成 ===")

if __name__ == "__main__":
    main()
