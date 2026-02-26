#!/usr/bin/env python3
"""
示例：图像识别点击
Example: Image recognition and click
"""

import sys
sys.path.insert(0, '..')

from desktop import DesktopController

def main():
    ctrl = DesktopController()
    
    print("=== 图像识别点击示例 ===\n")
    
    # 1. 截图
    print("1. 当前屏幕截图...")
    ctrl.screenshot_to_file("search.png")
    
    # 2. 尝试找图并点击
    # 注意：需要提前准备好按钮截图
    button_image = "submit_button.png"
    
    print(f"\n2. 查找图像: {button_image}")
    print("   (请确保图片存在，否则跳过)")
    
    # 示例代码（需要实际图片才能运行）
    # if ctrl.click_image(button_image, confidence=0.9):
    #     print("   ✓ 找到并点击按钮")
    # else:
    #     print("   ✗ 未找到按钮")
    
    print("\n=== 提示 ===")
    print("使用说明：")
    print("1. 先手动截图保存为 submit_button.png")
    print("2. 运行此脚本即可自动找图点击")
    print("\n需要安装 OpenCV: pip install opencv-python")

if __name__ == "__main__":
    main()
