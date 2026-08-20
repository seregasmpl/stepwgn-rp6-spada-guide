# -*- coding: utf-8 -*-
"""Build standalone Gathers LXM-247VFNi mini-site from guide sections."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
OUT_DIR = ROOT / "gathers"
OUT = OUT_DIR / "index.html"

PANEL_IDS = [
    "gathers-start",
    "gathers-keys",
    "gathers-home",
    "gathers-navi",
    "gathers-audio",
    "gathers-phone",
    "gathers-settings",
    "gathers-extra",
]

NAV = [
    ("gathers-start", "Быстрый старт"),
    ("gathers-keys", "Физические кнопки"),
    ("gathers-home", "HOME-меню"),
    ("gathers-navi", "Навигация / карта"),
    ("gathers-audio", "Аудио / диск / SD"),
    ("gathers-phone", "Телефон / Bluetooth"),
    ("gathers-settings", "設定／情報"),
    ("gathers-extra", "ETC / 後席会話 / камеры"),
]


def extract_panel(html: str, pid: str) -> str:
    m = re.search(
        rf'(<section id="{re.escape(pid)}" class="page-panel"[^>]*>.*?</section>)',
        html,
        flags=re.S,
    )
    if not m:
        raise SystemExit(f"missing panel {pid}")
    block = m.group(1)
    # fix relative img paths if any (none in gathers text) and nav links to other gathers
    block = block.replace('href="#honda-connect"', 'href="../index.html#honda-connect"')
    block = block.replace('href="#connect-hardware"', 'href="../index.html#connect-hardware"')
    block = block.replace('href="#cameras-multiview"', 'href="../index.html#cameras-multiview"')
    # remove data-nav-item from external links so they don't get intercepted as panels
    block = re.sub(
        r'<a data-nav-item href="\.\./index\.html#([^"]+)">',
        r'<a href="../index.html#\1">',
        block,
    )
    return block


def main():
    html = INDEX.read_text(encoding="utf-8")
    panels = []
    for i, pid in enumerate(PANEL_IDS):
        block = extract_panel(html, pid)
        if i == 0:
            # default panel id for app.js is "start"
            block = re.sub(r'id="gathers-start"', 'id="start"', block, count=1)
            if "is-active" not in block.split(">", 1)[0]:
                block = block.replace('class="page-panel"', 'class="page-panel is-active"', 1)
        else:
            block = re.sub(r'\s*is-active', "", block, count=1)
        panels.append(block)

    nav_items = "\n".join(
        f'        <li><a data-nav-item href="#{("start" if pid == "gathers-start" else pid)}">{label}</a></li>'
        for pid, label in NAV
    )

    page = f"""<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
  <meta name="apple-mobile-web-app-capable" content="yes" />
  <meta name="theme-color" content="#0b0f14" />
  <meta name="description" content="Gathers LXM-247VFNi — инструкция JP→RU (Honda CONNECT 9&quot;)" />
  <title>Gathers LXM-247VFNi — магнитола / нави (JP→RU)</title>
  <link rel="stylesheet" href="../assets/css/style.css" />
  <style>
    .site-switch {{
      display:flex; gap:8px; flex-wrap:wrap; margin:0 0 12px;
    }}
    .site-switch a {{
      display:inline-block; padding:10px 14px; border-radius:12px;
      border:1px solid var(--border); background:rgba(102,179,255,.12);
      color:var(--text); font-weight:600; text-decoration:none;
    }}
    .site-switch a:hover {{ text-decoration:none; border-color:rgba(102,179,255,.4) }}
    .site-switch .muted-link {{
      background:transparent; font-weight:500; color:var(--muted);
    }}
  </style>
</head>
<body>
  <div class="nav-backdrop" data-nav-backdrop hidden></div>

  <div class="wrap layout">
    <div class="content-col">
      <div class="panel-toolbar">
        <button type="button" class="nav-toggle" data-nav-toggle aria-label="Открыть меню" aria-expanded="false" aria-controls="guide-nav">
          <span class="nav-toggle-bars" aria-hidden="true"></span>
        </button>
        <button type="button" class="panel-btn" data-panel-prev aria-label="Предыдущий раздел">←</button>
        <p class="panel-head" data-panel-title aria-live="polite"><strong>—</strong></p>
        <button type="button" class="panel-btn" data-panel-next aria-label="Следующий раздел">→</button>
      </div>
      <div class="site-switch">
        <a href="./">LXM-247VFNi</a>
        <a class="muted-link" href="../">← STEP WGN (салон / приборка)</a>
      </div>
      <main class="main-scroll" data-main-scroll>
{chr(10).join(panels)}
      </main>
      <footer class="content-foot muted">
        Gathers LXM-247VFNi — отдельный справочник. Источник: Honda 取扱説明書.
        <a href="https://www.honda.co.jp/manual-access/navi/lxm-247vfni/" target="_blank" rel="noreferrer">PDF на honda.co.jp</a>
      </footer>
    </div>

    <aside class="nav" id="guide-nav" aria-label="Навигация">
      <div class="nav-drawer-head">
        <span class="nav-drawer-title">Магнитола</span>
        <button type="button" class="nav-close" data-nav-close aria-label="Закрыть меню">×</button>
      </div>
      <input data-nav-filter placeholder="Поиск…" />
      <div class="nav-scroll" data-nav-scroll>
      <ul data-nav-list>
        <li class="nav-group">LXM-247VFNi</li>
{nav_items}
        <li class="nav-group">Другое</li>
        <li><a href="../">STEP WGN — салон / БК</a></li>
      </ul>
      </div>
      <p class="nav-foot muted">☰ слева — разделы магнитолы.</p>
    </aside>
  </div>

  <script src="../assets/js/app.js"></script>
</body>
</html>
"""

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT.write_text(page, encoding="utf-8")
    print("wrote", OUT.relative_to(ROOT), "panels", len(panels))


if __name__ == "__main__":
    main()
