// 切換正序/倒序
function toggleOrder() {
  const list = document.getElementById("chapter-list");
  const items = Array.from(list.querySelectorAll("li"));
  items.reverse();
  list.innerHTML = "";
  items.forEach(item => list.appendChild(item));
}

// 回到頂部功能
function scrollToTop() {
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

// 滾動時顯示/隱藏回到頂部按鈕
window.addEventListener("scroll", () => {
  const btn = document.getElementById("back-to-top");
  if (!btn) return;
  if (window.scrollY > 200) {
    btn.style.display = "block";
  } else {
    btn.style.display = "none";
  }
});
