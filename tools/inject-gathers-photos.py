# -*- coding: utf-8 -*-
"""Inject Clicccar Honda CONNECT photos into gathers-* panels."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
BASE = "./assets/img/gathers-ru"
FALLBACK = "./assets/img/clicccar/1320797"


def fig(name: str, caption: str, alt: str | None = None) -> str:
    src_path = ROOT / "assets" / "img" / "gathers-ru" / name
    if not src_path.is_file():
        src = f"{FALLBACK}/{name}"
    else:
        src = f"{BASE}/{name}"
    a = alt or caption
    return (
        f'<figure><img src="{src}" alt="{a}" class="zoomable" '
        f'data-full="{src}" loading="lazy"><figcaption>{caption}</figcaption></figure>'
    )


def grid(*items: tuple[str, str]) -> str:
    figs = "\n          ".join(fig(n, c) for n, c in items)
    return f'\n        <div class="img-grid">\n          {figs}\n        </div>\n'


PHOTOS = {
    "gathers-start": grid(
        ("st15-cs-hc-0-main-we.jpg", "ГУ в салоне"),
        ("st15-cs-hc-1-honda-connect-switch-we.jpg", "Кнопки под экраном"),
        ("st15-cs-hc-2-home.jpg", "HOME — главная"),
    ),
    "gathers-keys": grid(
        ("st15-cs-hc-1-honda-connect-switch-we.jpg", "Ряд кнопок"),
        ("st15-cs-hc-1-honda-connect-switch.jpg", "Крупнее"),
        ("st15-cs-hc-6-talking-switch-we.jpg", "Разговор с задним рядом"),
    ),
    "gathers-home": grid(
        ("st15-cs-hc-2-home.jpg", "HOME"),
        ("st15-cs-hc-2-2-home.jpg", "Свайп иконок"),
        ("st15-cs-hc-3-home-1-navi-menu.jpg", "Меню навигации"),
        ("st15-cs-hc-3-2-home-2-Apple-CarPlay.jpg", "Apple CarPlay"),
        ("st15-cs-hc-3-3-home-3-Android-Auto.jpg", "Android Auto"),
        ("st15-cs-hc-3-4-home-4-telephone.jpg", "Телефон"),
        ("st15-cs-hc-3-5-home-5-setting-and-information.jpg", "Настройки / Инфо"),
        ("st15-cs-hc-3-6-home-6-Honda-Total-Care.jpg", "Honda Total Care"),
        ("st15-cs-hc-3-7-home-7-Audio-Source.jpg", "Источник аудио"),
        ("st15-cs-hc-3-8-home-8-owners-manual.jpg", "Руководство"),
        ("st15-cs-hc-3-9-home-9-Wi-Fi.jpg", "Wi‑Fi в салоне"),
        ("st15-cs-hc-3-10-home-10-clock.jpg", "Часы"),
        ("st15-cs-hc-3-11-home-11-menu-custmize.jpg", "Настройка HOME"),
        ("st15-cs-hc-3-14-home-14-PM2.5.jpg", "PM2.5"),
        ("st15-cs-hc-3-15-home-15-multi-view-camera.jpg", "Камеры"),
    ),
    "gathers-navi": grid(
        ("st15-cs-hc-3-home-1-navi-menu.jpg", "Меню навигации"),
        ("st15-cs-hc-7-owners-manual.jpg", "Руководство в мониторе"),
        ("st15-cs-hc-7-2-owners-manual.jpg", "Разделы руководства"),
        ("st15-cs-hc-7-4-owners-manual.jpg", "Поиск в руководстве"),
    ),
    "gathers-audio": grid(
        ("st15-cs-hc-3-7-home-7-Audio-Source.jpg", "Источник аудио"),
        ("st15-cs-hc-3-7-2-home-7-Audio-Source.jpg", "Список источников"),
        ("st15-cs-hc-3-7-3-home-7-Audio-Source.jpg", "Источники"),
        ("st15-cs-hc-5-2-set-and-info-2-av.jpg", "Настройки AV"),
        ("st15-cs-hc-5-2-1-set-and-info-2-av-1-sound-setting.jpg", "Звук"),
        ("st15-cs-hc-5-7-3-set-and-info-7-volume-set-3-audio.jpg", "Громкость аудио"),
    ),
    "gathers-phone": grid(
        ("st15-cs-hc-3-4-home-4-telephone.jpg", "Телефон"),
        ("st15-cs-hc-3-4-2-home-4-telephone.jpg", "Экран телефона"),
        ("st15-cs-hc-5-4-set-and-info-4-bluetooth-and-internavi-set.jpg", "Bluetooth / InterNavi"),
        ("st15-cs-hc-5-4-1-set-and-info-4-bluetooth-and-internavi-set-1-bluetooth.jpg", "Bluetooth"),
        ("st15-cs-hc-5-3-2-set-and-info-3-info-set-2-phone-set.jpg", "Настройки телефона"),
        ("st15-cs-hc-5-7-2-set-and-info-7-volume-set-2-telephone.jpg", "Громкость телефона"),
    ),
    "gathers-settings": grid(
        ("st15-cs-hc-3-5-home-5-setting-and-information.jpg", "Настройки / Инфо"),
        ("st15-cs-hc-5-set-and-info.jpg", "7 пунктов настроек"),
        ("st15-cs-hc-5-2-set-and-info-2-av.jpg", "AV"),
        ("st15-cs-hc-5-3-set-and-info-3-info-set.jpg", "Информация"),
        ("st15-cs-hc-5-4-set-and-info-4-bluetooth-and-internavi-set.jpg", "Bluetooth"),
        ("st15-cs-hc-5-5-set-and-info-5-system-setting.jpg", "Система"),
        ("st15-cs-hc-5-5-2-set-and-info-5-system-setting-2-hard-key.jpg", "Физ. кнопки"),
        ("st15-cs-hc-5-5-2-2-set-and-info-5-system-setting-2-2-steering-switch.jpg", "Кнопки руля"),
        ("st15-cs-hc-5-5-3-set-and-info-5-system-setting-3-clock-set.jpg", "Часы"),
        ("st15-cs-hc-5-5-5-set-and-info-5-system-setting-5-camera.jpg", "Камера"),
        ("st15-cs-hc-5-6-set-and-info-6-ipod-setting.jpg", "iPod"),
        ("st15-cs-hc-5-7-1-set-and-info-7-volume-set-1-system.jpg", "Громкость система"),
    ),
    "gathers-extra": grid(
        ("st15-cs-hc-5-3-3-set-and-info-3-info-set-3-etc-set.jpg", "ETC"),
        ("st15-cs-hc-6-talking-switch-we.jpg", "Разговор сзади"),
        ("st15-cs-hc-5-7-4-set-and-info-7-volume-set-4-taliking-with-rear-passenger-system.jpg", "Громкость разговора"),
        ("st15-cs-hc-3-15-home-15-multi-view-camera.jpg", "Multi-View"),
        ("st15-cs-hc-3-15-2-home-15-multi-view-camera.jpg", "Камера"),
        ("st15-cs-hc-3-14-home-14-PM2.5.jpg", "PM2.5"),
        ("st15-cs-hc-3-6-home-6-Honda-Total-Care.jpg", "Honda Total Care"),
        ("st15-cs-hc-5-5-5-set-and-info-5-system-setting-5-camera.jpg", "Настройка камеры"),
    ),
}

MARKER = "<!-- gathers-photos -->"


def inject(html: str, pid: str, photos: str) -> str:
    # remove old injected block if re-run
    html = re.sub(
        rf'(<section id="{re.escape(pid)}"[\s\S]*?){re.escape(MARKER)}[\s\S]*?{re.escape(MARKER)}\s*',
        r"\1",
        html,
        count=1,
    )
    # insert after <h2>...</h2>
    pat = rf'(<section id="{re.escape(pid)}" class="page-panel"[^>]*>\s*<h2>[^<]*</h2>)'
    repl = rf"\1\n        {MARKER}{photos}        {MARKER}"
    new_html, n = re.subn(pat, repl, html, count=1)
    if n != 1:
        raise SystemExit(f"failed inject {pid}")
    return new_html


def main():
    html = INDEX.read_text(encoding="utf-8")
    for pid, photos in PHOTOS.items():
        html = inject(html, pid, photos)
    INDEX.write_text(html, encoding="utf-8")
    print("injected", len(PHOTOS), "panels")


if __name__ == "__main__":
    main()
