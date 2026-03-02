# Desktop Control Skill for OpenClaw

Windows Desktop Automation via AI | Windows 桌面 AI 自动化控制

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform: Windows](https://img.shields.io/badge/Platform-Windows-blue.svg)](https://www.microsoft.com/windows)
[![Python: 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Stars](https://img.shields.io/github/stars/1578606997-dotcom/desktop-control-skill)](https://github.com/1578606997-dotcom/desktop-control-skill/stargazers)

> 🎉 **我们刚刚发布了浏览器插件版本！** 现在可以在 Chrome 中直接控制浏览器了。
> 
> 💬 **[加入讨论](https://github.com/1578606997-dotcom/desktop-control-skill/discussions)** - 分享你的使用场景，最佳分享者将获得 Contributor 身份！

---

## 🎯 项目简介

这是一个 **OpenClaw Skill**，让 AI 能够直接控制 Windows 桌面——就像有一双"眼睛"和"手"。

**核心功能：**
- 👁️ **视觉**：截图、图像识别
- 🖱️ **操作**：鼠标点击、移动、拖拽
- ⌨️ **输入**：键盘输入、快捷键
- 🧠 **智能**：AI 看懂屏幕，自动决策

---

## 👥 作者

**Original Framework | 原始框架**  
[Jhong Cai](https://github.com/1578606997-dotcom) - 架构设计、核心概念

**Refinement & OpenClaw Integration | 完善与 OpenClaw 集成**  
[OpenClaw AI](https://github.com/openclaw) - 代码优化、Skill 封装、文档完善

**Development Collaboration | 开发协作**  
本项目由人类开发者与 AI 助手共同完成，展示了人机协作的新模式。

---

## 🚀 快速开始

### 安装

```bash
# 1. 克隆仓库
git clone https://github.com/1578606997-dotcom/desktop-control-skill.git
cd desktop-control-skill

# 2. 安装依赖
pip install -r requirements.txt

# 3. 作为 OpenClaw Skill 安装
openclaw skills add ./
```

### 基本使用

```bash
# 查看屏幕尺寸
openclaw skills run desktop-control screen_size

# 获取鼠标位置
openclaw skills run desktop-control mouse_pos

# 截图
openclaw skills run desktop-control screenshot --full

# 点击坐标
openclaw skills run desktop-control click --x 500 --y 300

# 输入文字
openclaw skills run desktop-control type --text "Hello World"

# 按下快捷键
openclaw skills run desktop-control keypress --hotkey ctrl,c
```

---

## 🎮 功能列表

### 屏幕操作
| 命令 | 功能 | 示例 |
|------|------|------|
| `screenshot` | 截图（区域/全屏） | `--x 0 --y 0 --w 1920 --h 1080` |
| `screen_size` | 获取屏幕尺寸 | 返回 `{width, height}` |
| `mouse_pos` | 获取鼠标位置 | 返回 `{x, y}` |

### 鼠标控制
| 命令 | 功能 | 参数 |
|------|------|------|
| `click` | 点击指定位置 | `--x 500 --y 300 --button left` |
| `move` | 移动鼠标 | `--x 500 --y 300 --duration 0.5` |
| `scroll` | 滚动 | `--clicks -5` (负数向下) |

### 键盘控制
| 命令 | 功能 | 示例 |
|------|------|------|
| `type` | 输入文字 | `--text "Hello" --interval 0.01` |
| `keypress` | 按键 | `--key enter` 或 `--hotkey ctrl,c` |

### 图像识别
| 命令 | 功能 | 说明 |
|------|------|------|
| `locate` | 找图 | `--image button.png --confidence 0.9` |
| `click_image` | 找图并点击 | `--image submit.png` |

---

## 💡 使用场景

### 场景 1：浏览器自动化
```python
# AI 自动操作浏览器
1. 截图查看当前页面
2. 识别"登录"按钮位置
3. 点击按钮
4. 输入用户名密码
5. 点击提交
```

### 场景 2：批量处理
```python
# 自动化重复任务
1. 打开应用
2. 点击菜单
3. 处理文件
4. 保存结果
5. 循环执行
```

### 场景 3：远程协助
```python
# AI 远程帮你操作电脑
- "帮我打开设置"
- "调整音量到50%"
- "关闭所有标签页"
```

---

## 🔧 技术栈

- **Python 3.8+** - 核心语言
- **pyautogui** - 鼠标键盘控制
- **mss** - 高性能截图
- **PIL/Pillow** - 图像处理
- **OpenCV** - 图像识别（可选）

---

## 🤝 如何参与

我们欢迎各种形式的贡献！

### 新手友好任务
- 📖 **完善文档**: 改进 README、添加使用示例
- 🐛 **报告 Bug**: 遇到问题直接提 Issue
- 💡 **功能建议**: 有什么想法尽管说
- 🌟 **点 Star**: 支持项目发展

### 参与方式
1. **Fork 项目**
2. **创建分支** (`git checkout -b feature/AmazingFeature`)
3. **提交更改** (`git commit -m 'Add some AmazingFeature'`)
4. **推送分支** (`git push origin feature/AmazingFeature`)
5. **创建 Pull Request**

### 讨论区
- [GitHub Discussions](../../discussions) - 闲聊、提问、分享
- [Issues](../../issues) - Bug 报告、功能请求

---

## 🛡️ 安全说明

**⚠️ 重要安全特性：**

1. **FAILSAFE 机制**：鼠标移到屏幕左上角立即终止
2. **DPI 感知**：自动适配 Windows 缩放设置
3. **操作间隔**：默认 50ms 延迟，防止过快操作
4. **坐标边界检查**：防止点击屏幕外

**使用建议：**
- 首次使用先测试简单操作
- 复杂任务建议先截图确认
- 不要在生产环境/重要数据上测试

---

## 🤝 贡献指南

欢迎贡献！无论是：
- 🐛 报告 Bug
- 💡 提出新功能
- 📝 改进文档
- 🔧 提交代码

请遵循：
1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

---

## 📜 许可证

[MIT License](./LICENSE)

Copyright (c) 2026 Jhong Cai & OpenClaw AI

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.

---

## 🙏 致谢

- [OpenClaw](https://github.com/openclaw) - 提供 AI 助手平台和工具框架
- [pyautogui](https://github.com/asweigart/pyautogui) - 底层自动化库
- [mss](https://github.com/BoboTiG/mss) - 高性能截图库

---

## 📮 联系方式

- **Issues**: [GitHub Issues](https://github.com/1578606997-dotcom/desktop-control-skill/issues)
- **Email**: [Your Email]
- **Twitter**: [Your Twitter]

---

<p align="center">
  <b>Built with ❤️ by Human + AI Collaboration</b><br>
  <i>人机协作，创造无限可能</i>
</p>
