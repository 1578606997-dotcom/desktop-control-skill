# Desktop Control - Browser Extension

浏览器自动化插件，支持截图、点击、输入、滚动等操作。

## 安装

### 方式一：Chrome Web Store（推荐）
待发布

### 方式二：手动安装（开发者模式）

1. 下载 `browser-extension` 文件夹
2. 打开 Chrome，访问 `chrome://extensions/`
3. 开启右上角"开发者模式"
4. 点击"加载已解压的扩展程序"
5. 选择 `browser-extension` 文件夹

## 功能

- 📸 **截图** - 捕获当前标签页
- 🖱️ **点击** - 点击元素（通过选择器或坐标）
- ⌨️ **输入** - 在输入框输入文字
- 📜 **滚动** - 滚动页面
- 📄 **页面信息** - 获取标题、URL、滚动位置等

## 与 OpenClaw 集成

1. 在弹出窗口中输入 OpenClaw Gateway URL
2. 点击"连接 OpenClaw"
3. 现在可以通过 OpenClaw AI 控制浏览器了

## 文件结构

```
browser-extension/
├── manifest.json      # 插件配置
├── background.js      # 后台服务
├── content.js         # 内容脚本
├── popup.html         # 弹出界面
├── popup.js           # 弹出逻辑
└── icons/             # 图标（待添加）
```

## 开发

```bash
# 加载到 Chrome
1. 打开 chrome://extensions/
2. 开启开发者模式
3. 加载已解压的扩展程序

# 调试
- 点击"service worker"查看 background.js 日志
- 在网页按 F12，查看 content.js 日志
```

## 从 Python 版本迁移

原 Python 版本（控制桌面）→ 浏览器版本（控制浏览器）

| 功能 | Python 版本 | 浏览器版本 |
|------|------------|-----------|
| 截图 | 全屏/区域 | 当前标签页 |
| 点击 | 桌面坐标 | 网页元素 |
| 输入 | 系统输入 | 网页输入框 |
| 适用 | 桌面自动化 | 网页自动化 |

## 作者

- **框架设计**: Jhong Cai
- **代码实现**: OpenClaw AI
- **项目**: https://github.com/1578606997-dotcom/desktop-control-skill
