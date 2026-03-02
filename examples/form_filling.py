#!/usr/bin/env python3
"""
示例：自动化表单填写
Example: Automated form filling
"""

import sys
import time
sys.path.insert(0, '..')

from desktop import DesktopController

def main():
    ctrl = DesktopController()
    
    print("=== 表单自动填写示例 ===\n")
    
    # 示例数据
    form_data = [
        {"x": 100, "y": 200, "text": "张三"},
        {"x": 100, "y": 250, "text": "test@example.com"},
        {"x": 100, "y": 300, "text": "13800138000"},
    ]
    
    # 1. 打开目标应用/网页
    print("1. 聚焦到目标窗口...")
    time.sleep(1)
    
    # 2. 逐个填写字段
    print("2. 填写表单数据...")
    for i, field in enumerate(form_data, 1):
        # 点击目标位置
        ctrl.click(x=field["x"], y=field["y"])
        time.sleep(0.3)
        
        # 输入文字
        ctrl.type(field["text"])
        time.sleep(0.3)
        
        print(f"   字段 {i}: {field['text']}")
    
    # 3. 点击提交按钮
    print("\n3. 点击提交按钮...")
    ctrl.click(x=100, y=400)
    
    print("\n=== 完成 ===")

if __name__ == "__main__":
    main()
