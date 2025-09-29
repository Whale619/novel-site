// main.js

// ================= 字體大小切換 =================
function setFontSize(size) {
  let root = document.body;

  // 桌面版字體大小控制
  if (window.innerWidth > 768 && !root.classList.contains("mobile")) {
    if (size === 'small') root.style.fontSize = "16px";   // 小字體
    else if (size === 'medium') root.style.fontSize = "18px"; // 中字體
    else if (size === 'large') root.style.fontSize = "20px";  // 大字體
  } 
  // 手機版字體大小控制（字體較大）
  else {
    if (size === 'small') root.style.fontSize = "18px";
    else if (size === 'medium') root.style.fontSize = "20px";
    else if (size === 'large') root.style.fontSize = "22px";
  }

  // 將目前字體大小選擇存入 localStorage，方便下次載入自動套用
  localStorage.setItem('readerFontSize', size);
}

// ================= 主題切換 =================
function toggleTheme() {
  let body = document.body;
  body.classList.toggle("light"); // 切換 light 模式（暗 ↔ 亮）

  // 判斷目前主題狀態，存入 localStorage
  let theme = body.classList.contains("light") ? "light" : "dark";
  localStorage.setItem('readerTheme', theme);
}

// ================= DOM 載入後執行 =================
document.addEventListener("DOMContentLoaded", () => {
  // 偵測是否為行動裝置，若是則加上 "mobile" 樣式標記
  let isMobile = /Mobi|Android|iPhone|iPad|iPod/i.test(navigator.userAgent);
  if (isMobile) {
    document.body.classList.add("mobile");
  }

  // 載入字體大小設定，若沒有紀錄則預設為 medium
  let savedSize = localStorage.getItem('readerFontSize');
  if (!savedSize) savedSize = 'medium';
  setFontSize(savedSize);

  // 載入主題設定，若沒有紀錄則預設為 dark
  let savedTheme = localStorage.getItem('readerTheme') || 'dark';
  if (savedTheme === 'light') document.body.classList.add("light");
});

// ================= 回到頂部 =================
function scrollToTop() {
  // 平滑滾動到頁面最上方
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ================= 章節排序切換 =================
function toggleOrder() {
  const list = document.getElementById("chapter-list");
  if (!list) return;

  // 取得章節清單的所有 <li> 元素，並反轉順序
  const items = Array.from(list.querySelectorAll("li"));
  items.reverse();

  // 清空原本的清單，重新插入反轉後的章節
  list.innerHTML = "";
  items.forEach(item => list.appendChild(item));
}
