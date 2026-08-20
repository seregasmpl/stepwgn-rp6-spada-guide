# -*- coding: utf-8 -*-
"""Inject ALL gathers-ru photos into gathers panels + rewrite main guide paths."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
RU = ROOT / "assets" / "img" / "gathers-ru"
BASE = "./assets/img/gathers-ru"
MARKER = "<!-- gathers-photos -->"

CAPTIONS = {
    "st15-cs-hc-0-main-we.jpg": "ГУ в салоне",
    "st15-cs-hc-1-honda-connect-switch-we.jpg": "Экран и кнопки",
    "st15-cs-hc-1-honda-connect-switch.jpg": "Экран и кнопки",
    "st15-cs-hc-2-home.jpg": "HOME",
    "st15-cs-hc-2-2-home.jpg": "HOME — свайп",
    "st15-cs-hc-6-talking-switch-we.jpg": "Разговор сзади",
}


def caption(name: str) -> str:
    if name in CAPTIONS:
        return CAPTIONS[name]
    # strip prefix noise
    n = name.replace("st15-cs-hc-", "").replace(".jpg", "")
    return n.replace("-", " ")[:48]


def fig(name: str) -> str:
    src = f"{BASE}/{name}"
    c = caption(name)
    return (
        f'<figure><img src="{src}" alt="{c}" class="zoomable" '
        f'data-full="{src}" loading="lazy"><figcaption>{c}</figcaption></figure>'
    )


def grid(names: list[str]) -> str:
    figs = "\n          ".join(fig(n) for n in names if (RU / n).is_file())
    return f'\n        <div class="img-grid">\n          {figs}\n        </div>\n'


def classify(name: str) -> str:
    n = name.lower()
    if name.startswith("st15-cs-hc-0") or name.startswith("st15-cs-hc-1"):
        return "gathers-start"
    if "talking" in n or name.startswith("st15-cs-hc-6"):
        return "gathers-keys"
    if "honda-connect-switch" in n:
        return "gathers-keys"
    if "owners-manual" in n or name.startswith("st15-cs-hc-7"):
        return "gathers-navi"
    if "navi-menu" in n or "navi" in n and "home-1" in n:
        return "gathers-navi"
    if "audio" in n or "-av" in n or "sound" in n or "dvd" in n or "recording" in n or "ipod" in n:
        return "gathers-audio"
    if "telephone" in n or "phone" in n or "bluetooth" in n:
        return "gathers-phone"
    if "etc" in n or "pm2.5" in n or "camera" in n or "parking" in n or "total-care" in n:
        return "gathers-extra"
    if "set-and-info" in n or "system-setting" in n or "volume-set" in n:
        return "gathers-settings"
    if "home" in n:
        return "gathers-home"
    return "gathers-extra"


def inject(html: str, pid: str, photos: str) -> str:
    html = re.sub(
        rf'(<section id="{re.escape(pid)}"[\s\S]*?){re.escape(MARKER)}[\s\S]*?{re.escape(MARKER)}\s*',
        r"\1",
        html,
        count=1,
    )
    pat = rf'(<section id="{re.escape(pid)}" class="page-panel"[^>]*>\s*<h2>[^<]*</h2>)'
    repl = rf"\1\n        {MARKER}{photos}        {MARKER}"
    new_html, n = re.subn(pat, repl, html, count=1)
    if n != 1:
        raise SystemExit(f"inject fail {pid}")
    return new_html


def rewrite_main_guide_paths(html: str) -> str:
    def repl(m: re.Match) -> str:
        attr = m.group(1)
        path = m.group(2)
        name = Path(path).name
        base = re.sub(r"-\d+x\d+(?=\.jpg$)", "", name, flags=re.I)
        if (RU / base).is_file():
            return f'{attr}="./assets/img/gathers-ru/{base}"'
        if (RU / name).is_file():
            return f'{attr}="./assets/img/gathers-ru/{name}"'
        return m.group(0)

    return re.sub(
        r'(src|data-full)="(\./assets/img/clicccar/1320797/[^"]+)"',
        repl,
        html,
    )


def ru_captions_in_honda_connect(html: str) -> str:
    """Replace leftover JP figcaptions near gathers-ru images in main CONNECT panels."""
    reps = [
        (">ナビ<", ">Навигация<"),
        (">設定／情報<", ">Настройки / Инфо<"),
        (">取扱説明書<", ">Руководство<"),
        (">AV設定<", ">Настройки AV<"),
        (">情報設定<", ">Настройки информации<"),
        (">システム設定<", ">Системные настройки<"),
        (">リスト 7 пунктов<", ">7 пунктов настроек<"),
        (">список 7 пунктов<", ">7 пунктов настроек<"),
    ]
    for a, b in reps:
        html = html.replace(a, b)
    return html


def main():
    buckets: dict[str, list[str]] = {k: [] for k in (
        "gathers-start", "gathers-keys", "gathers-home", "gathers-navi",
        "gathers-audio", "gathers-phone", "gathers-settings", "gathers-extra",
    )}
    for name in sorted(p.name for p in RU.glob("*.jpg")):
        buckets[classify(name)].append(name)

    # Force overview + key panels to share important shots
    for n in (
        "st15-cs-hc-0-main-we.jpg",
        "st15-cs-hc-1-honda-connect-switch-we.jpg",
        "st15-cs-hc-1-honda-connect-switch.jpg",
        "st15-cs-hc-2-home.jpg",
        "st15-cs-hc-5-set-and-info.jpg",
    ):
        if (RU / n).is_file() and n not in buckets["gathers-start"]:
            buckets["gathers-start"].insert(0, n)
    for n in (
        "st15-cs-hc-1-honda-connect-switch-we.jpg",
        "st15-cs-hc-1-honda-connect-switch.jpg",
        "st15-cs-hc-6-talking-switch-we.jpg",
    ):
        if (RU / n).is_file() and n not in buckets["gathers-keys"]:
            buckets["gathers-keys"].append(n)

    prefer = [
        "st15-cs-hc-0-main-we.jpg",
        "st15-cs-hc-1-honda-connect-switch-we.jpg",
        "st15-cs-hc-2-home.jpg",
        "st15-cs-hc-5-set-and-info.jpg",
    ]
    start = buckets["gathers-start"]
    buckets["gathers-start"] = [n for n in prefer if (RU / n).is_file()] + [
        n for n in start if n not in prefer
    ]

    html = INDEX.read_text(encoding="utf-8")
    for pid, names in buckets.items():
        seen = set()
        uniq = []
        for n in names:
            if n not in seen:
                seen.add(n)
                uniq.append(n)
        html = inject(html, pid, grid(uniq))
    html = rewrite_main_guide_paths(html)
    html = ru_captions_in_honda_connect(html)
    INDEX.write_text(html, encoding="utf-8")
    print("ok", {k: len(v) for k, v in buckets.items()})


if __name__ == "__main__":
    main()
