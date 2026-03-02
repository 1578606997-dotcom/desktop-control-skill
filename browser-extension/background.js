// background.js - Service Worker
// 处理来自 OpenClaw 或 popup 的消息，转发到 content script

// 监听来自 popup 的消息
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  console.log('Background received:', request);
  
  switch (request.action) {
    case 'screenshot':
      captureScreenshot(sendResponse);
      return true; // 保持通道开放
      
    case 'click':
      executeInActiveTab('click', request.params, sendResponse);
      return true;
      
    case 'type':
      executeInActiveTab('type', request.params, sendResponse);
      return true;
      
    case 'scroll':
      executeInActiveTab('scroll', request.params, sendResponse);
      return true;
      
    case 'getPageInfo':
      executeInActiveTab('getPageInfo', {}, sendResponse);
      return true;
      
    case 'findAndClick':
      executeInActiveTab('findAndClick', request.params, sendResponse);
      return true;
      
    default:
      sendResponse({error: 'Unknown action: ' + request.action});
  }
});

// 捕获当前标签页截图
async function captureScreenshot(sendResponse) {
  try {
    const tab = await getActiveTab();
    const dataUrl = await chrome.tabs.captureVisibleTab(tab.windowId, {
      format: 'png',
      quality: 90
    });
    
    // 转换为 base64
    const base64 = dataUrl.split(',')[1];
    
    sendResponse({
      success: true,
      format: 'png',
      base64: base64,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    sendResponse({
      success: false,
      error: error.message
    });
  }
}

// 在活跃标签页执行操作
async function executeInActiveTab(action, params, sendResponse) {
  try {
    const tab = await getActiveTab();
    
    const results = await chrome.scripting.executeScript({
      target: { tabId: tab.id },
      func: executeAction,
      args: [action, params]
    });
    
    sendResponse(results[0].result);
  } catch (error) {
    sendResponse({
      success: false,
      error: error.message
    });
  }
}

// 获取当前活跃标签页
function getActiveTab() {
  return new Promise((resolve, reject) => {
    chrome.tabs.query({active: true, currentWindow: true}, (tabs) => {
      if (tabs.length === 0) {
        reject(new Error('No active tab'));
      } else {
        resolve(tabs[0]);
      }
    });
  });
}

// 在网页上下文中执行操作
function executeAction(action, params) {
  switch (action) {
    case 'click':
      return clickElement(params);
    case 'type':
      return typeText(params);
    case 'scroll':
      return scrollPage(params);
    case 'getPageInfo':
      return getPageInfo();
    case 'findAndClick':
      return findAndClick(params);
    default:
      return {error: 'Unknown action'};
  }
}

// 点击元素（通过坐标或选择器）
function clickElement(params) {
  try {
    if (params.selector) {
      const el = document.querySelector(params.selector);
      if (!el) return {success: false, error: 'Element not found'};
      el.click();
      return {success: true, action: 'click', selector: params.selector};
    } else if (params.x !== undefined && params.y !== undefined) {
      const el = document.elementFromPoint(params.x, params.y);
      if (!el) return {success: false, error: 'No element at position'};
      el.click();
      return {success: true, action: 'click', x: params.x, y: params.y};
    }
    return {success: false, error: 'No selector or coordinates provided'};
  } catch (error) {
    return {success: false, error: error.message};
  }
}

// 输入文字
function typeText(params) {
  try {
    const el = document.activeElement;
    if (!el || !['INPUT', 'TEXTAREA'].includes(el.tagName)) {
      // 尝试找到第一个可输入元素
      el = document.querySelector('input, textarea');
    }
    if (!el) return {success: false, error: 'No input element found'};
    
    el.value = params.text;
    el.dispatchEvent(new Event('input', {bubbles: true}));
    el.dispatchEvent(new Event('change', {bubbles: true}));
    
    return {success: true, action: 'type', text: params.text};
  } catch (error) {
    return {success: false, error: error.message};
  }
}

// 滚动页面
function scrollPage(params) {
  try {
    const scrollAmount = params.amount || 300;
    window.scrollBy({
      top: scrollAmount,
      behavior: 'smooth'
    });
    return {
      success: true,
      action: 'scroll',
      amount: scrollAmount,
      newScrollY: window.scrollY
    };
  } catch (error) {
    return {success: false, error: error.message};
  }
}

// 获取页面信息
function getPageInfo() {
  return {
    success: true,
    title: document.title,
    url: window.location.href,
    scrollY: window.scrollY,
    scrollHeight: document.body.scrollHeight,
    viewport: {
      width: window.innerWidth,
      height: window.innerHeight
    },
    elementCount: document.querySelectorAll('*').length
  };
}

// 查找文本并点击
function findAndClick(params) {
  try {
    const text = params.text;
    const elements = document.querySelectorAll('*');
    
    for (const el of elements) {
      if (el.textContent.includes(text) && el.click) {
        el.click();
        return {success: true, action: 'findAndClick', text: text, found: true};
      }
    }
    
    return {success: false, error: 'Text not found: ' + text};
  } catch (error) {
    return {success: false, error: error.message};
  }
}

// 连接 OpenClaw（如果配置了）
let ws = null;
let openclawConnected = false;

function connectToOpenClaw(config) {
  if (ws) {
    ws.close();
  }
  
  ws = new WebSocket(config.url);
  
  ws.onopen = () => {
    console.log('Connected to OpenClaw');
    openclawConnected = true;
    ws.send(JSON.stringify({
      type: 'register',
      agent: 'browser_extension',
      capabilities: ['screenshot', 'click', 'type', 'scroll']
    }));
  };
  
  ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    handleOpenClawCommand(data);
  };
  
  ws.onerror = (error) => {
    console.error('OpenClaw connection error:', error);
    openclawConnected = false;
  };
  
  ws.onclose = () => {
    console.log('OpenClaw connection closed');
    openclawConnected = false;
  };
}

// 处理来自 OpenClaw 的命令
function handleOpenClawCommand(data) {
  chrome.runtime.sendMessage({
    action: data.action,
    params: data.params
  }, (response) => {
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({
        type: 'result',
        id: data.id,
        result: response
      }));
    }
  });
}

// 导出供 popup 使用
chrome.runtime.onConnect.addListener((port) => {
  if (port.name === 'openclaw') {
    port.onMessage.addListener((msg) => {
      if (msg.action === 'connect') {
        connectToOpenClaw(msg.config);
      }
    });
  }
});
