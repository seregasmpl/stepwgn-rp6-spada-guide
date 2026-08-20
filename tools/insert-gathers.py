# -*- coding: utf-8 -*-
from pathlib import Path

root = Path(__file__).resolve().parents[1]
index = root / "index.html"
snip = (root / "tools" / "gathers-lxm-247vfni-snippet.html").read_text(encoding="utf-8")
html = index.read_text(encoding="utf-8")

marker = '      <section id="controls-everywhere" class="page-panel" data-panel>'
if 'id="gathers-start"' in html:
    print("already inserted")
else:
    if marker not in html:
        raise SystemExit("marker missing")
    html = html.replace(marker, snip + "\n" + marker, 1)

old_nav = """        <li class=\"nav-group\">Honda CONNECT</li>
        <li><a data-nav-item href=\"#honda-connect\">HOME + 設定／情報</a></li>
        <li><a class=\"sub\" data-nav-item href=\"#connect-hardware\">Кнопки под экраном</a></li>"""

new_nav = """        <li class=\"nav-group\">Gathers LXM-247VFNi</li>
        <li><a data-nav-item href=\"#gathers-start\">Быстрый старт ГУ</a></li>
        <li><a class=\"sub\" data-nav-item href=\"#gathers-keys\">Физические кнопки</a></li>
        <li><a class=\"sub\" data-nav-item href=\"#gathers-home\">HOME-меню</a></li>
        <li><a class=\"sub\" data-nav-item href=\"#gathers-navi\">Навигация / карта</a></li>
        <li><a class=\"sub\" data-nav-item href=\"#gathers-audio\">Аудио / диск / SD</a></li>
        <li><a class=\"sub\" data-nav-item href=\"#gathers-phone\">Телефон / Bluetooth</a></li>
        <li><a class=\"sub\" data-nav-item href=\"#gathers-settings\">設定／情報</a></li>
        <li><a class=\"sub\" data-nav-item href=\"#gathers-extra\">ETC / 後席会話 / камеры</a></li>
        <li><a class=\"sub\" data-nav-item href=\"#honda-connect\">↳ фото HOME + настройки</a></li>
        <li><a class=\"sub\" data-nav-item href=\"#connect-hardware\">↳ фото кнопок</a></li>"""

if "Gathers LXM-247VFNi" not in html:
    if old_nav not in html:
        raise SystemExit("nav block missing")
    html = html.replace(old_nav, new_nav, 1)

# sources + glossary
src_line = '          <li><b>Gathers LXM-247VFNi</b> (офиц. OM + 簡単操作): <a href="https://www.honda.co.jp/manual-access/navi/lxm-247vfni/" target="_blank" rel="noreferrer">honda.co.jp/manual-access/navi/lxm-247vfni</a></li>\n'
if "LXM-247VFNi" not in html.split("id=\"sources\"")[1][:2000]:
    html = html.replace(
        '          <li><b>Honda CONNECT (практика/меню)</b>',
        src_line + '          <li><b>Honda CONNECT (практика/меню)</b>',
        1,
    )

gloss_rows = """            <tr><td><span class=\"kbd\">現在地</span></td><td>текущее место на карте</td></tr>
            <tr><td><span class=\"kbd\">目的地検索</span></td><td>поиск цели маршрута</td></tr>
            <tr><td><span class=\"kbd\">案内開始</span></td><td>начать ведение маршрута</td></tr>
            <tr><td><span class=\"kbd\">オフフック</span></td><td>снять трубку / позвонить</td></tr>
            <tr><td><span class=\"kbd\">後席会話サポート</span></td><td>голос в задние динамики</td></tr>
            <tr><td><span class=\"kbd\">モニター Open</span></td><td>открыть панель диска/SD</td></tr>
"""
if "目的地検索" not in html.split("id=\"glossary\"")[1][:2500]:
    html = html.replace(
        '            <tr><td><span class="kbd">設定／情報</span></td><td>настройки и информация</td></tr>',
        '            <tr><td><span class="kbd">設定／情報</span></td><td>настройки и информация</td></tr>\n' + gloss_rows,
        1,
    )

html = html.replace("v1.4", "v1.5", 1)
html = html.replace("v1.4.", "v1.5.", 1)

index.write_text(html, encoding="utf-8")
print("written", index)
print("panels", sum(1 for x in ["gathers-start","gathers-keys","gathers-home","gathers-navi","gathers-audio","gathers-phone","gathers-settings","gathers-extra"] if f'id="{x}"' in html))
