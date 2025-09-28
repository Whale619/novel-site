import re
from pathlib import Path

# 資料夾設定
TXT_DIR = Path("txt_sources")
CHAPTER_DIR = Path("chapters")
CHAPTER_DIR.mkdir(exist_ok=True)
INDEX_FILE = Path("index.html")

# 替換引號（將 "..." 或 '...' → 「...」）
def replace_quotes(text: str) -> str:
    # 雙引號
    text = re.sub(r'"([^"]*?)"', r'「\1」', text)
    # 單引號
    text = re.sub(r"'([^']*?)'", r'「\1」', text)
    return text

# 清理規則
def clean_line(line: str) -> str | None:
    line = line.strip()
    if not line:
        return None
    # 刪掉含有「漢化」「漢 化」「閒魚」
    if re.search(r"漢\s*化", line) or "閒魚" in line:
        return None
    if "@雨" in line:
        return None
    if re.fullmatch(r"[A-Za-z0-9]+", line):
        return None

    # 特殊替換
    line = line.replace("清明", "青明")
    line = replace_quotes(line)
    return line

# 判斷章節標題
def parse_chapter_title(line: str) -> str | None:
    m = re.match(r".*?(?:第)?(\d+)(章|話|回)([^一-龥]*)(.*)", line)
    if m:
        num = m.group(1)
        text = m.group(4).strip()
        # 不論原本是「話/回」，一律轉換成「章」
        if text:
            return f"第{num}章 - {text}"
        else:
            return f"第{num}章"
    return None

# 處理 txt → 切章
def process_txt(file_path: Path):
    chapters = []
    current_title = None
    current_lines = []

    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for raw in lines:
        line = clean_line(raw)
        if line is None:
            continue

        title = parse_chapter_title(line)
        if title:
            # 取出數字部分（判斷章節號）
            current_num = re.match(r"第(\d+)章", title)
            prev_num = re.match(r"第(\d+)章", current_title) if current_title else None

            # 如果章節號一樣，保留新的（覆蓋掉舊的）
            if current_title and prev_num and current_num and prev_num.group(1) == current_num.group(1):
                current_title = title
                current_lines = []  # 清空內容，用新章節取代
                continue

            # 正常換章
            if current_title and current_lines:
                chapters.append((current_title, "\n".join(current_lines)))
            current_title = title
            current_lines = []
            continue
        else:
            current_lines.append(line)

    if current_title and current_lines:
        chapters.append((current_title, "\n".join(current_lines)))

    return chapters

# 生成章節 HTML
def write_chapters(chapters):
    html_template = """<!DOCTYPE html>
<html lang="zh-Hant">
<head>
  <meta charset="UTF-8">
  <link rel="stylesheet" href="../css/style.css">
  <title>{title}</title>
  <link rel="icon" href="../img/favicon.ico" type="image/x-icon">
</head>
<body>
<div class="nav">
  <a href="../index.html">返回目錄</a> | {prev_link} | {next_link}
</div>
<h1>{title}</h1>
<div class="content">
{content}
</div>
<div class="nav">
  <a href="../index.html">返回目錄</a> | {prev_link} | {next_link}
</div>
<button id="back-to-top" onclick="scrollToTop()">▲ 回到頂部</button>
<script src="../js/main.js"></script>
</body>
</html>"""

    for idx, (title, content) in enumerate(chapters, start=1):
        prev_link = f'<a href="{idx-1}.html">上一章</a>' if idx > 1 else "上一章"
        next_link = f'<a href="{idx+1}.html">下一章</a>' if idx < len(chapters) else "下一章"
        chapter_html = html_template.format(
            title=title,
            content="<p>" + "</p><p>".join(content.split("\n")) + "</p>",
            prev_link=prev_link,
            next_link=next_link,
        )
        with open(CHAPTER_DIR / f"{idx}.html", "w", encoding="utf-8") as f:
            f.write(chapter_html)

# 生成首頁 HTML
def write_index(chapters):
    html = """<!DOCTYPE html>
<html lang="zh-Hant">
<head>
  <meta charset="UTF-8">
  <link rel="stylesheet" href="css/style.css">
  <title>화산귀환 - 小說翻譯</title>
  <script src="js/main.js" defer></script>
  <link rel="icon" href="img/favicon.ico" type="image/x-icon">
</head>
<body>
<div class="book-info">
  <div class="cover">
    <img src="img/cover.jpg" alt="封面">
  </div>
  <div class="meta">
    <h1>《화산귀환 - 劍尊歸來》</h1>
    <p><b>作者：</b> 비가</p>
    <p><b>狀態：</b> 連載中</p>
    <p><b>簡介：</b><br>
        斬下禍亂天下的天魔的首級後，華山派梅花劍尊青明在十萬大山的山頂長眠。<br>
        再睜眼，竟已百年過去，他更以少年的身軀重生。<br>
        青明回到華山，只見當年盛極一時的華山派──<br>
        啪！沒了？！<br>
        於是，大華山派第十三代弟子梅花劍尊，成了華山派最後一個新進小師弟，<br>
        在復興門派的道路上，展開了孤軍奮鬥。
    </p>
  </div>
</div>

<h2>小說目錄</h2>
<button onclick="toggleOrder()">切換正序/倒序</button>
<ul id="chapter-list">
"""
    for idx, (title, _) in enumerate(chapters, start=1):
        html += f'<li><a href="chapters/{idx}.html">{title}</a></li>\n'
    html += """</ul>
<button id="back-to-top" onclick="scrollToTop()">▲ 回到頂部</button>
<script src="js/main.js"></script>
</body>
</html>"""
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        f.write(html)

# 主程式
def main():
    def extract_number(path: Path):
        m = re.search(r'(\d+)', path.name)
        return int(m.group(1)) if m else 0

    all_chapters = []
    for txt_file in sorted(TXT_DIR.glob("*.txt"), key=extract_number):
        all_chapters.extend(process_txt(txt_file))
    write_chapters(all_chapters)
    write_index(all_chapters)

    print(f"✅ 轉換完成！共 {len(all_chapters)} 章")

if __name__ == "__main__":
    main()
