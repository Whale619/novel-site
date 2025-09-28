function setFontSize(size) {
  let root = document.body;

  if (window.innerWidth > 768 && !root.classList.contains("mobile")) {
    // 電腦版（不變）
    if (size === 'small') root.style.fontSize = "16px";
    else if (size === 'medium') root.style.fontSize = "18px";
    else if (size === 'large') root.style.fontSize = "20px";
  } else {
    // 手機版 ✅ 放大
    if (size === 'small') root.style.fontSize = "22px";
    else if (size === 'medium') root.style.fontSize = "24px";
    else if (size === 'large') root.style.fontSize = "28px";
  }
  localStorage.setItem('readerFontSize', size);
}

function toggleTheme() {
  let body = document.body;
  body.classList.toggle("light");
  let theme = body.classList.contains("light") ? "light" : "dark";
  localStorage.setItem('readerTheme', theme);
}

document.addEventListener("DOMContentLoaded", () => {
  let isMobile = /Mobi|Android|iPhone|iPad|iPod/i.test(navigator.userAgent);
  if (isMobile) {
    document.body.classList.add("mobile");
  }

  let savedSize = localStorage.getItem('readerFontSize');
  if (!savedSize) savedSize = 'medium';
  setFontSize(savedSize);

  let savedTheme = localStorage.getItem('readerTheme') || 'dark';
  if (savedTheme === 'light') document.body.classList.add("light");
});

function scrollToTop() {
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

function toggleOrder() {
  const list = document.getElementById("chapter-list");
  if (!list) return;
  const items = Array.from(list.querySelectorAll("li"));
  items.reverse();
  list.innerHTML = "";
  items.forEach(item => list.appendChild(item));
}