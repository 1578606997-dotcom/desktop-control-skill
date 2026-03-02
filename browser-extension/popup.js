// popup.js - 浏览器插件弹出界面逻辑

document.addEventListener('DOMContentLoaded', () => {
  const btnScreenshot = document.getElementById('btnScreenshot');
  const btnClick = document.getElementById('btnClick');
  const btnType = document.getElementById('btnType');
  const btnScroll = document.getElementById('btnScroll');
  const btnInfo = document.getElementById('btnInfo');
  const btnConnect = document.getElementById('btnConnect');
  const result = document.getElementById('result');
  const resultContent = document.getElementById('resultContent');
  const statusDot = document.getElementById('statusDot');
  const statusText = document.getElementById('statusText');
  const gatewayUrl = document.getElementById('gatewayUrl');
  
  // 显示结果
  function showResult(data) {
    result.style.display = 'block';
    resultContent.textContent = JSON.stringify(data, null, 2);
  }
  
  // 更新状态
  function updateStatus(text, isError = false) {
    statusText.textContent = text;
    statusDot.style.background = isError ? '#ef4444' : '#4ade80';
  }
  
  // 截图
  btnScreenshot.addEventListener('click', async () => {
    updateStatus('截图中...');
    try {
      const response = await chrome.runtime.sendMessage({action: 'screenshot'});
      if (response.success) {
        showResult({
          action: 'screenshot',
          format: response.format,
          base64_length: response.base64 ? response.base64.length : 0,
          timestamp: response.timestamp
        });
        
        // 可选：下载截图
        if (response.base64) {
          const link = document.createElement('a');
          link.href = 'data:image/png;base64,' + response.base64;
          link.download = 'screenshot_' + Date.now() + '.png';
          link.click();
        }
        
        updateStatus('截图成功');
      } else {
        showResult(response);
        updateStatus('截图失败', true);
      }
    } catch (error) {
      showResult({error: error.message});
      updateStatus('错误', true);
    }
  });
  
  // 点击元素
  btnClick.addEventListener('click', async () => {
    const selector = prompt('输入 CSS 选择器或坐标 (x,y):', 'button');
    if (!selector) return;
    
    updateStatus('点击中...');
    try {
      let params = {};
      if (selector.includes(',')) {
        const [x, y] = selector.split(',').map(Number);
        params = {x, y};
      } else {
        params = {selector};
      }
      
      const response = await chrome.runtime.sendMessage({
        action: 'click',
        params: params
      });
      showResult(response);
      updateStatus(response.success ? '点击成功' : '点击失败', !response.success);
    } catch (error) {
      showResult({error: error.message});
      updateStatus('错误', true);
    }
  });
  
  // 输入文字
  btnType.addEventListener('click', async () => {
    const text = prompt('输入要输入的文字:', 'Hello World');
    if (!text) return;
    
    updateStatus('输入中...');
    try {
      const response = await chrome.runtime.sendMessage({
        action: 'type',
        params: {text}
      });
      showResult(response);
      updateStatus(response.success ? '输入成功' : '输入失败', !response.success);
    } catch (error) {
      showResult({error: error.message});
      updateStatus('错误', true);
    }
  });
  
  // 滚动页面
  btnScroll.addEventListener('click', async () => {
    const amount = prompt('输入滚动距离 (正数向下，负数向上):', '500');
    if (!amount) return;
    
    updateStatus('滚动中...');
    try {
      const response = await chrome.runtime.sendMessage({
        action: 'scroll',
        params: {amount: parseInt(amount)}
      });
      showResult(response);
      updateStatus(response.success ? '滚动成功' : '滚动失败', !response.success);
    } catch (error) {
      showResult({error: error.message});
      updateStatus('错误', true);
    }
  });
  
  // 获取页面信息
  btnInfo.addEventListener('click', async () => {
    updateStatus('获取信息中...');
    try {
      const response = await chrome.runtime.sendMessage({
        action: 'getPageInfo'
      });
      showResult(response);
      updateStatus('获取成功');
    } catch (error) {
      showResult({error: error.message});
      updateStatus('错误', true);
    }
  });
  
  // 连接 OpenClaw
  btnConnect.addEventListener('click', () => {
    const url = gatewayUrl.value.trim() || 'ws://127.0.0.1:18789';
    
    updateStatus('连接中...');
    
    // 存储配置
    chrome.storage.local.set({openclawUrl: url}, () => {
      console.log('OpenClaw URL saved:', url);
    });
    
    // 尝试连接
    const port = chrome.runtime.connect({name: 'openclaw'});
    port.postMessage({
      action: 'connect',
      config: {url: url}
    });
    
    port.onMessage.addListener((msg) => {
      if (msg.connected) {
        updateStatus('已连接 OpenClaw');
      } else {
        updateStatus('连接失败', true);
      }
    });
    
    setTimeout(() => {
      updateStatus('连接超时，请检查 OpenClaw 是否运行', true);
    }, 5000);
  });
  
  // 加载保存的配置
  chrome.storage.local.get(['openclawUrl'], (result) => {
    if (result.openclawUrl) {
      gatewayUrl.value = result.openclawUrl;
    }
  });
});
