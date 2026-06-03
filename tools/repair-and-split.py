# -*- coding: utf-8 -*-
import re
from pathlib import Path

root = Path(__file__).resolve().parents[1]
src = root / "index.html"
text = src.read_text(encoding="utf-8")

head_m = re.search(
    r"(?s)(.*?</section>\s*)\s*(?:<!-- legacy[^>]*-->)?\s*<section id=\"controls-everywhere\"",
    text,
)
head = head_m.group(1)

inner_m = re.search(
    r'(?s)<section id="controls-everywhere"[^>]*>(.*?)(?=\s*<section id="controls-everywhere")',
    text,
)
controls_inner = inner_m.group(1).strip()

tail_m = re.search(r'(?s)(\s*<section id="adas-wheel".*)', text)
tail = tail_m.group(1)

# Split at h3 boundaries
h3_pat = re.compile(r'<h3(?:\s+id="([^"]*)")?[^>]*>(.*?)</h3>', re.S)
matches = list(h3_pat.finditer(controls_inner))
overview = controls_inner[: matches[0].start()].strip() if matches else controls_inner

chunks = []
for i, m in enumerate(matches):
    end = matches[i + 1].start() if i + 1 < len(matches) else len(controls_inner)
    pid = m.group(1) or ""
    title = re.sub(r"<[^>]+>", "", m.group(2)).strip()
    if not pid:
        if "ENGINE START" in title:
            pid = "engine-start"
        else:
            pid = re.sub(r"[^\w-]+", "-", title.lower())[:40].strip("-")
    body = controls_inner[m.end() : end].strip()
    chunks.append((pid, title, body))

panels = [
    f'''      <section id="controls-everywhere" class="page-panel" data-panel>
        <h2>Органы управления: обзор салона</h2>
{overview}
      </section>'''
]
for pid, title, body in chunks:
    panels.append(
        f'''      <section id="{pid}" class="page-panel" data-panel>
        <h2>{title}</h2>
{body}
      </section>'''
    )

panels.append(
    '''      <section id="cameras-multiview" class="page-panel" data-panel>
        <h2>Камеры и Multi-View Camera</h2>
        <div class="two-col">
          <div class="ru">
            <b>Кнопка CAM</b> (центральная консоль, если установлена): камера при движении вперёд на малой скорости.<br/>
            <b>R</b>: задняя камера + линии траектории; настройка линий: Honda CONNECT → <span class="kbd">設定／情報</span> → <span class="kbd">システム設定</span> → камера.<br/>
            <b>Multi-View</b>: вид «сверху» вокруг машины — удобно в узких местах и у бордюра.
          </div>
        </div>
        <p class="muted">Фото MVC — см. Clicccar 9‑11; при отсутствии файла в папке assets откройте статью 1315602.</p>
      </section>'''
)

panels.append(
    '''      <section id="tire-angle" class="page-panel" data-panel>
        <h2>Монитор угла колёс (タイヤ角度モニター)</h2>
        <p>7 ступеней поворота передних колёс. Появляется при большом угле руля на <span class="kbd">D</span>/<span class="kbd">S</span>/<span class="kbd">R</span> или при включении с поворотом &gt;90°.</p>
        <p><b>Вкл/выкл</b>: правый MID → <span class="kbd">車両設定</span> → <span class="kbd">メーター設定</span> → <span class="kbd">タイヤ角度モニター</span>.</p>
        <div class="img-grid">
          <figure><img src="./assets/img/clicccar/1312122/st8-ut-6-tire-angle-monitor-we-200x136.jpg" alt="tire" loading="lazy"/><figcaption>углы колёс</figcaption></figure>
          <figure><img src="./assets/img/clicccar/1312122/st8-ut-6-2-tire-angle-monitor-we-200x136.jpg" alt="tire2" loading="lazy"/><figcaption>другой ракурс</figcaption></figure>
        </div>
      </section>'''
)

out = head + "\n".join(panels) + "\n" + tail
out = re.sub(
    r'<section id="([^"]+)" class="page-panel"(?!\s+data-panel)',
    r'<section id="\1" class="page-panel" data-panel',
    out,
)

src.write_text(out, encoding="utf-8")
print("ok panels:", len(chunks), [c[0] for c in chunks])
