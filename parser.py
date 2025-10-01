# parser.py
import re
from pathlib import Path

# 來源資料夾與輸出資料夾
TXT_DIR = Path("txt_sources")     # 原始小說TXT檔資料夾
CHAPTER_DIR = Path("chapters")    # 輸出 HTML 章節檔的資料夾
CHAPTER_DIR.mkdir(exist_ok=True)  # 若資料夾不存在就建立
INDEX_FILE = Path("index.html")   # 目錄頁檔案名稱

# 將 "" 或 '' 轉換為「」
def replace_quotes(text: str) -> str:
    text = re.sub(r'"([^"]*?)"', r'「\1」', text)  # 把雙引號替換成中文引號
    text = re.sub(r"'([^']*?)'", r'「\1」', text)  # 把單引號替換成中文引號
    return text

# 清理單行文字
def clean_line(line: str) -> str | None:
    line = line.strip()              # 移除前後空白
    if not line: return None         # 跳過空行

    # 過濾雜訊/無關字樣
    if re.search(r"漢\s*化", line) or "閒魚" in line: return None
    if "@雨" in line: return None
    if re.fullmatch(r"[A-Za-z0-9]+", line): return None  # 跳過純英數字

    # 特殊字替換
    line = line.replace("清明", "青明")
    line = line.replace("清字", "青字")
    line = line.replace("素素", "小小")
    line = line.replace("唐保", "唐步")
    line = line.replace("道士師兄", "道士大哥")
    line = line.replace("紫目草", "紫木草")
    line = line.replace("四叔", "師叔")
    line = line.replace("玄用", "玄從")
    line = line.replace("運字", "雲字")
    line = line.replace("韓哲", "寒玄")
    line = line.replace("四哥", "師姑")
    line = line.replace("!", "！")
    line = line.replace("?", "？")

    return replace_quotes(line)      # 最後替換引號

# 偵測章節標題
def parse_chapter_title(line: str) -> str | None:
    if re.match(r'^\s*序\s*$', line):   # 特殊情況：僅「序」
        return "序"

    # 一般章節標題（例：第X章）
    m = re.match(r".*?(?:第)?(\d+)(章|話|回)([^一-龥]*)(.*)", line)
    if m:
        num = m.group(1)              # 章節數字
        text = m.group(4).strip()     # 章節標題文字
        return f"第{num}章 - {text}" if text else f"第{num}章"
    return None

# 解析TXT，輸出章節內容
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
            # 判斷是否為同一章重複
            current_num = re.match(r"第(\d+)章", title)
            prev_num = re.match(r"第(\d+)章", current_title) if current_title else None

            if current_title and prev_num and current_num and prev_num.group(1) == current_num.group(1):
                # 如果前後章節號碼相同，更新標題但不新增內容
                current_title, current_lines = title, []
                continue

            # 儲存上一章
            if current_title and current_lines:
                chapters.append((current_title, "\n".join(current_lines)))

            # 開始新章節
            current_title, current_lines = title, []
            continue
        else:
            current_lines.append(line)   # 章節內文行

    # 加入最後一章
    if current_title and current_lines:
        chapters.append((current_title, "\n".join(current_lines)))

    return chapters

# 生成各章節HTML
def write_chapters(chapters):
    # 單章頁面HTML樣板
    html_template = """<!DOCTYPE html>
<html lang="zh-Hant">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0"> <!-- 🔹 加這行 -->
  <link rel="stylesheet" href="../css/style.css">
  <title>{title}</title>
  <link rel="icon" href="../img/favicon.ico" type="image/x-icon">
</head>
<body>

<!-- 控制列 (內頁)-->
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

<!-- 上一章 / 下一章 -->
<div class="nav">
  {prev_link}
  {next_link}
</div>

<h1>{title}</h1>
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

    # 逐章生成 HTML
    for idx, (title, content) in enumerate(chapters, start=1):
        prev_link = f'<a href="{idx-1}.html">上一章</a>' if idx > 1 else '<span>上一章</span>'
        next_link = f'<a href="{idx+1}.html">下一章</a>' if idx < len(chapters) else '<span>下一章</span>'

        # 插入章節內容，每行用 <p> 包裹
        chapter_html = html_template.format(
            title=title,
            content="<p>" + "</p><p>".join(content.split("\n")) + "</p>",
            prev_link=prev_link,
            next_link=next_link,
        )

        # 寫出 HTML 檔
        with open(CHAPTER_DIR / f"{idx}.html", "w", encoding="utf-8") as f:
            f.write(chapter_html)

# 生成首頁目錄
def write_index(chapters):
    html = """<!DOCTYPE html>
<html lang="zh-Hant">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0"> <!-- 🔹 加這行 -->
  <link rel="stylesheet" href="css/style.css">
  <title>화산귀환 - 劍尊歸來</title>
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

<!-- 控制列 -->
<div class="controls">
  <div class="controls-left">
    <button onclick="toggleOrder()">切換正序/倒序</button>
  </div>
  <div class="controls-right">
    <button onclick="toggleTheme()">切換主題</button>
  </div>
</div>

<h2>小說目錄</h2>
<ul id="chapter-list">
"""
    # 插入所有章節連結
    for idx, (title, _) in enumerate(chapters, start=1):
        html += f'<li><a href="chapters/{idx}.html">{title}</a></li>\n'

    html += """</ul>
<button id="back-to-top" onclick="scrollToTop()">▲ 回到頂部</button>
<script src="js/main.js"></script>
</body>
</html>"""

    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        f.write(html)

# 主流程
def main():
    # 從檔名取數字做排序依據
    def extract_number(path: Path):
        m = re.search(r'(\d+)', path.name)
        return int(m.group(1)) if m else 0

    all_chapters = []
    # 讀取所有 TXT 檔，依數字排序
    for txt_file in sorted(TXT_DIR.glob("*.txt"), key=extract_number):
        all_chapters.extend(process_txt(txt_file))

    # 輸出章節 HTML & 目錄頁
    write_chapters(all_chapters)
    write_index(all_chapters)
    print(f"✅ 轉換完成！共 {len(all_chapters)} 章")

if __name__ == "__main__":
    main()
