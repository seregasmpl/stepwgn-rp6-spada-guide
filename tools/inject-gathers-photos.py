# -*- coding: utf-8 -*-
"""Inject Clicccar Honda CONNECT photos into gathers-* panels."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
BASE = "./assets/img/clicccar/1320797"


def fig(name: str, caption: str, alt: str | None = None) -> str:
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
        ("st15-cs-hc-0-main-we.jpg", "ГУ / салон"),
        ("st15-cs-hc-1-honda-connect-switch-we.jpg", "кнопки под экраном"),
        ("st15-cs-hc-2-home.jpg", "HOME"),
    ),
    "gathers-keys": grid(
        ("st15-cs-hc-1-honda-connect-switch-we.jpg", "ряд hard key"),
        ("st15-cs-hc-1-honda-connect-switch.jpg", "крупнее"),
        ("st15-cs-hc-6-talking-switch-we.jpg", "後席会話 (кнопка)"),
    ),
    "gathers-home": grid(
        ("st15-cs-hc-2-home.jpg", "HOME"),
        ("st15-cs-hc-2-2-home.jpg", "свайп иконок"),
        ("st15-cs-hc-3-home-1-navi-menu.jpg", "ナビメニュー"),
        ("st15-cs-hc-3-2-home-2-Apple-CarPlay.jpg", "Apple CarPlay"),
        ("st15-cs-hc-3-3-home-3-Android-Auto.jpg", "Android Auto"),
        ("st15-cs-hc-3-4-home-4-telephone.jpg", "電話"),
        ("st15-cs-hc-3-5-home-5-setting-and-information.jpg", "設定／情報"),
        ("st15-cs-hc-3-6-home-6-Honda-Total-Care.jpg", "Honda Total Care"),
        ("st15-cs-hc-3-7-home-7-Audio-Source.jpg", "Audio Source"),
        ("st15-cs-hc-3-8-home-8-owners-manual.jpg", "取扱説明書"),
        ("st15-cs-hc-3-9-home-9-Wi-Fi.jpg", "車内Wi-Fi"),
        ("st15-cs-hc-3-10-home-10-clock.jpg", "時計"),
        ("st15-cs-hc-3-11-home-11-menu-custmize.jpg", "カスタマイズ HOME"),
        ("st15-cs-hc-3-14-home-14-PM2.5.jpg", "PM2.5"),
        ("st15-cs-hc-3-15-home-15-multi-view-camera.jpg", "カメラ / Multi-View"),
    ),
    "gathers-navi": grid(
        ("st15-cs-hc-3-home-1-navi-menu.jpg", "ナビメニュー"),
        ("st15-cs-hc-7-owners-manual.jpg", "取説 в мониторе"),
        ("st15-cs-hc-7-2-owners-manual.jpg", "разделы мануала"),
        ("st15-cs-hc-7-4-owners-manual.jpg", "поиск в мануале"),
    ),
    "gathers-audio": grid(
        ("st15-cs-hc-3-7-home-7-Audio-Source.jpg", "Audio Source"),
        ("st15-cs-hc-3-7-2-home-7-Audio-Source.jpg", "источники"),
        ("st15-cs-hc-3-7-3-home-7-Audio-Source.jpg", "источники (ещё)"),
        ("st15-cs-hc-5-2-set-and-info-2-av.jpg", "AV設定"),
        ("st15-cs-hc-5-2-1-set-and-info-2-av-1-sound-setting.jpg", "звуковые настройки"),
        ("st15-cs-hc-5-7-3-set-and-info-7-volume-set-3-audio.jpg", "音量・オーディオ"),
    ),
    "gathers-phone": grid(
        ("st15-cs-hc-3-4-home-4-telephone.jpg", "電話"),
        ("st15-cs-hc-3-4-2-home-4-telephone.jpg", "телефон (экран)"),
        ("st15-cs-hc-5-4-set-and-info-4-bluetooth-and-internavi-set.jpg", "Bluetooth／インターナビ"),
        ("st15-cs-hc-5-4-1-set-and-info-4-bluetooth-and-internavi-set-1-bluetooth.jpg", "Bluetooth設定"),
        ("st15-cs-hc-5-3-2-set-and-info-3-info-set-2-phone-set.jpg", "電話の設定"),
        ("st15-cs-hc-5-7-2-set-and-info-7-volume-set-2-telephone.jpg", "音量・電話"),
    ),
    "gathers-settings": grid(
        ("st15-cs-hc-3-5-home-5-setting-and-information.jpg", "иконка 設定／情報"),
        ("st15-cs-hc-5-set-and-info.jpg", "7 пунктов настроек"),
        ("st15-cs-hc-5-2-set-and-info-2-av.jpg", "AV設定"),
        ("st15-cs-hc-5-3-set-and-info-3-info-set.jpg", "情報設定"),
        ("st15-cs-hc-5-4-set-and-info-4-bluetooth-and-internavi-set.jpg", "Bluetooth"),
        ("st15-cs-hc-5-5-set-and-info-5-system-setting.jpg", "システム設定"),
        ("st15-cs-hc-5-5-2-set-and-info-5-system-setting-2-hard-key.jpg", "ハードキー"),
        ("st15-cs-hc-5-5-2-2-set-and-info-5-system-setting-2-2-steering-switch.jpg", "ステアリング"),
        ("st15-cs-hc-5-5-3-set-and-info-5-system-setting-3-clock-set.jpg", "時計"),
        ("st15-cs-hc-5-5-5-set-and-info-5-system-setting-5-camera.jpg", "カメラ"),
        ("st15-cs-hc-5-6-set-and-info-6-ipod-setting.jpg", "iPod設定"),
        ("st15-cs-hc-5-7-1-set-and-info-7-volume-set-1-system.jpg", "音量・システム"),
    ),
    "gathers-extra": grid(
        ("st15-cs-hc-5-3-3-set-and-info-3-info-set-3-etc-set.jpg", "ETC設定"),
        ("st15-cs-hc-6-talking-switch-we.jpg", "後席会話スイッチ"),
        ("st15-cs-hc-5-7-4-set-and-info-7-volume-set-4-taliking-with-rear-passenger-system.jpg", "音量・後席会話"),
        ("st15-cs-hc-3-15-home-15-multi-view-camera.jpg", "Multi-View"),
        ("st15-cs-hc-3-15-2-home-15-multi-view-camera.jpg", "камера (экран)"),
        ("st15-cs-hc-3-14-home-14-PM2.5.jpg", "PM2.5"),
        ("st15-cs-hc-3-6-home-6-Honda-Total-Care.jpg", "Honda Total Care"),
        ("st15-cs-hc-5-5-5-set-and-info-5-system-setting-5-camera.jpg", "настройка камеры"),
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
