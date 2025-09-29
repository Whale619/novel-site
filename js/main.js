// main.js

// ================= 字體大小切換 =================
function setFontSize(size) {
  let root = document.body;

  if (window.innerWidth > 768 && !root.classList.contains("mobile")) {
    // 桌面版字體
    if (size === 'small') root.style.fontSize = "16px";
    else if (size === 'medium') root.style.fontSize = "18px";
    else if (size === 'large') root.style.fontSize = "20px";
  } else {
    // 手機版字體更大
    if (size === 'small') root.style.fontSize = "18px";
    else if (size === 'medium') root.style.fontSize = "20px";
    else if (size === 'large') root.style.fontSize = "22px";
  }
  localStorage.setItem('readerFontSize', size); // 記錄到本地
}

// ================= 手機板用：下拉選單字體切換 =================
function changeFontSize(size) {
  setFontSize(size);
  localStorage.setItem('readerFontSize', size); // 記錄選擇
}

// ================= 主題切換 =================
function toggleTheme() {
  let body = document.body;
  body.classList.toggle("light"); // 切換light模式
  let theme = body.classList.contains("light") ? "light" : "dark";
  localStorage.setItem('readerTheme', theme); // 儲存
}

// ================= DOM載入後執行 =================
document.addEventListener("DOMContentLoaded", () => {
  // 偵測裝置
  let isMobile = /Mobi|Android|iPhone|iPad|iPod/i.test(navigator.userAgent);
  if (isMobile) {
    document.body.classList.add("mobile");
  }

  // 載入字體大小設定
  let savedSize = localStorage.getItem('readerFontSize');
  if (!savedSize) savedSize = 'medium';
  setFontSize(savedSize);

  // 同步下拉選單狀態（手機版）
  let fontSelector = document.getElementById("fontSizeSelector");
  if (fontSelector) fontSelector.value = savedSize;

  // 載入主題設定
  let savedTheme = localStorage.getItem('readerTheme') || 'dark';
  if (savedTheme === 'light') document.body.classList.add("light");
});

// ================= 回到頂部 =================
function scrollToTop() {
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ================= 章節排序切換 =================
function toggleOrder() {
  const list = document.getElementById("chapter-list");
  if (!list) return;
  const items = Array.from(list.querySelectorAll("li"));
  items.reverse();                // 反轉順序
  list.innerHTML = "";
  items.forEach(item => list.appendChild(item));
}
