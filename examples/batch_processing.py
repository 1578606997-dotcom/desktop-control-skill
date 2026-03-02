#!/usr/bin/env python3
"""
示例：批量文件处理
Example: Batch file processing
"""

import sys
import os
import glob
import time
sys.path.insert(0, '..')

from desktop import DesktopController

def main():
    ctrl = DesktopController()
    
    print("=== 批量文件处理示例 ===\n")
    
    # 配置
    input_dir = "~/Downloads"
    file_pattern = "*.txt"
    
    # 1. 获取文件列表
    print("1. 扫描文件...")
    files = glob.glob(os.path.join(os.path.expanduser(input_dir), file_pattern))
    print(f"   找到 {len(files)} 个文件")
    
    # 2. 逐个处理
    print("\n2. 批量处理文件...")
    for i, filepath in enumerate(files, 1):
        filename = os.path.basename(filepath)
        
        # 模拟：点击文件、打开、处理
        print(f"   [{i}/{len(files)}] 处理: {filename}")
        
        # 实际操作时：
        # ctrl.double_click(x=100, y=200 + i*30)  # 点击文件
        # time.sleep(2)
        # ctrl.hotkey('alt', 'f4')  # 关闭
    
    print(f"\n=== 完成 {len(files)} 个文件 ===")

if __name__ == "__main__":
    main()
