import re
from pathlib import Path

TXT_DIR = Path("txt_sources")
CHAPTER_DIR = Path("chapters")
CHAPTER_DIR.mkdir(exist_ok=True)
INDEX_FILE = Path("index.html")

def replace_quotes(text: str) -> str:
    text = re.sub(r'"([^"]*?)"', r'「\1」', text)
    text = re.sub(r"'([^']*?)'", r'「\1」', text)
    return text

def clean_line(line: str) -> str | None:
    line = line.strip()
    if not line: return None
    if re.search(r"漢\s*化", line) or "閒魚" in line: return None
    if "@雨" in line: return None
    if re.fullmatch(r"[A-Za-z0-9]+", line): return None
    line = line.replace("清明", "青明")
    return replace_quotes(line)

def parse_chapter_title(line: str) -> str | None:
    # 特殊情況：序
    if re.match(r'^\s*序\s*$', line):
        return "序"
    # 一般章節
    m = re.match(r".*?(?:第)?(\d+)(章|話|回)([^一-龥]*)(.*)", line)
    if m:
        num = m.group(1)
        text = m.group(4).strip()
        return f"第{num}章 - {text}" if text else f"第{num}章"
    return None

def process_txt(file_path: Path):
    chapters = []
    current_title, current_lines = None, []
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    for raw in lines:
        line = clean_line(raw)
        if line is None: continue
        title = parse_chapter_title(line)
        if title:
            current_num = re.match(r"第(\d+)章", title)
            prev_num = re.match(r"第(\d+)章", current_title) if current_title else None
            if current_title and prev_num and current_num and prev_num.group(1) == current_num.group(1):
                current_title, current_lines = title, []
                continue
            if current_title and current_lines:
                chapters.append((current_title, "\n".join(current_lines)))
            current_title, current_lines = title, []
            continue
        else:
            current_lines.append(line)
    if current_title and current_lines:
        chapters.append((current_title, "\n".join(current_lines)))
    return chapters

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

<!-- ✅ 控制列（手機版會顯示在最上方） -->
<div class="controls">
  <div class="controls-left">
    <a href="../index.html">返回目錄</a>
  </div>
  <div class="controls-right">
    <button onclick="setFontSize('small')">小</button>
    <button onclick="setFontSize('medium')">中</button>
    <button onclick="setFontSize('large')">大</button>
    <button onclick="toggleTheme()">切換主題</button>
  </div>
</div>

<!-- 章節標題 -->
<h1>{title}</h1>

<!-- 上一章 / 下一章（標題下方） -->
<div class="nav">
  {prev_link}
  {next_link}
</div>

<div class="content">
{content}
</div>

<!-- 底部的上一章 / 下一章 -->
<div class="nav">
  {prev_link}
  {next_link}
</div>

<button id="back-to-top" onclick="scrollToTop()">▲ 回到頂部</button>
<script src="../js/main.js"></script>
</body>
</html>"""
    for idx, (title, content) in enumerate(chapters, start=1):
        prev_link = f'<a href="{idx-1}.html">⬅ 上一章</a>' if idx > 1 else '<span>⬅ 上一章</span>'
        next_link = f'<a href="{idx+1}.html">下一章 ➡</a>' if idx < len(chapters) else '<span>下一章 ➡</span>'
        chapter_html = html_template.format(
            title=title,
            content="<p>" + "</p><p>".join(content.split("\n")) + "</p>",
            prev_link=prev_link,
            next_link=next_link,
        )
        with open(CHAPTER_DIR / f"{idx}.html", "w", encoding="utf-8") as f:
            f.write(chapter_html)

def write_index(chapters):
    html = """<!DOCTYPE html>
<html lang="zh-Hant">
<head>
  <meta charset="UTF-8">
  <link rel="stylesheet" href="css/style.css">
  <title>화산귀환 - 劍尊歸來</title>
  <script src="js/main.js" defer></script>
  <link rel="icon" href="img/favicon.ico" type="image/x-icon">
</head>
<body>

<!-- ✅ 控制列（手機版會顯示在最上方） -->
<div class="controls">
  <div class="controls-left">
    <button onclick="toggleOrder()">切換正序/倒序</button>
  </div>
  <div class="controls-right">
    <button onclick="setFontSize('small')">小</button>
    <button onclick="setFontSize('medium')">中</button>
    <button onclick="setFontSize('large')">大</button>
    <button onclick="toggleTheme()">切換主題</button>
  </div>
</div>

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
