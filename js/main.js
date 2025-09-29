// main.js

// ================= 字體大小切換 =================
function setFontSize(size) {
  let root = document.body;

  if (window.innerWidth > 768 && !root.classList.contains("mobile")) {
    // 桌面版字體設定
    if (size === 'small') root.style.fontSize = "16px";
    else if (size === 'medium') root.style.fontSize = "18px";
    else if (size === 'large') root.style.fontSize = "20px";
  } else {
    // 手機版字體（較大）
    if (size === 'small') root.style.fontSize = "18px";
    else if (size === 'medium') root.style.fontSize = "20px";
    else if (size === 'large') root.style.fontSize = "22px";
  }

  localStorage.setItem('readerFontSize', size); // 記錄選擇到本地
}

// ================= 主題切換 =================
function toggleTheme() {
  let body = document.body;
  body.classList.toggle("light"); // 切換 light 模式
  let theme = body.classList.contains("light") ? "light" : "dark";
  localStorage.setItem('readerTheme', theme); // 儲存主題設定
}

// ================= DOM 載入後執行 =================
document.addEventListener("DOMContentLoaded", () => {
  // 偵測裝置：若是手機或平板，加上 mobile 樣式
  let isMobile = /Mobi|Android|iPhone|iPad|iPod/i.test(navigator.userAgent);
  if (isMobile) {
    document.body.classList.add("mobile");
  }

  // 載入字體大小設定（若無紀錄則預設 medium）
  let savedSize = localStorage.getItem('readerFontSize');
  if (!savedSize) savedSize = 'medium';
  setFontSize(savedSize);

  // 載入主題設定（若無紀錄則預設 dark）
  let savedTheme = localStorage.getItem('readerTheme') || 'dark';
  if (savedTheme === 'light') document.body.classList.add("light");
});

// ================= 回到頂部 =================
function scrollToTop() {
  window.scrollTo({ top: 0, behavior: 'smooth' }); // 平滑滾動到最上方
}

// ================= 章節排序切換 =================
function toggleOrder() {
  const list = document.getElementById("chapter-list");
  if (!list) return;

  const items = Array.from(list.querySelectorAll("li")); // 取得所有章節
  items.reverse();                // 反轉順序

  list.innerHTML = "";            // 清空原有清單
  items.forEach(item => list.appendChild(item)); // 重新加入
}
