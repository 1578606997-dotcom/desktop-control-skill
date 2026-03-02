// content.js - 注入到网页的脚本
// 用于与页面交互

console.log('Desktop Control: Content script loaded');

// 监听来自 background 的消息
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  console.log('Content script received:', request);
  
  switch (request.action) {
    case 'highlightElement':
      highlightElement(request.selector);
      sendResponse({success: true});
      break;
      
    case 'getElementText':
      const text = getElementText(request.selector);
      sendResponse({success: true, text});
      break;
      
    case 'fillForm':
      fillForm(request.data);
      sendResponse({success: true});
      break;
      
    default:
      sendResponse({error: 'Unknown action in content script'});
  }
  
  return true;
});

// 高亮元素
function highlightElement(selector) {
  const el = document.querySelector(selector);
  if (!el) return;
  
  const originalOutline = el.style.outline;
  el.style.outline = '3px solid #e94560';
  
  setTimeout(() => {
    el.style.outline = originalOutline;
  }, 2000);
}

// 获取元素文本
function getElementText(selector) {
  const el = document.querySelector(selector);
  return el ? el.textContent.trim() : null;
}

// 填充表单
function fillForm(data) {
  for (const [selector, value] of Object.entries(data)) {
    const el = document.querySelector(selector);
    if (el) {
      el.value = value;
      el.dispatchEvent(new Event('input', {bubbles: true}));
    }
  }
}

// 导出供页面内脚本使用
window.DesktopControl = {
  highlight: highlightElement,
  getText: getElementText,
  fillForm: fillForm
};
