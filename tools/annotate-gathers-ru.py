# -*- coding: utf-8 -*-
"""Burn Russian labels onto Gathers / Honda CONNECT screenshots."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "assets" / "img" / "clicccar" / "1320797"
OUT = ROOT / "assets" / "img" / "gathers-ru"
OUT.mkdir(parents=True, exist_ok=True)

# Icon closeups: cover JP caption band, draw RU
ICON_RU = {
    "st15-cs-hc-3-home-1-navi-menu.jpg": "Меню навигации",
    "st15-cs-hc-3-2-home-2-Apple-CarPlay.jpg": "Apple CarPlay",
    "st15-cs-hc-3-3-home-3-Android-Auto.jpg": "Android Auto",
    "st15-cs-hc-3-4-home-4-telephone.jpg": "Телефон",
    "st15-cs-hc-3-4-2-home-4-telephone.jpg": "Телефон",
    "st15-cs-hc-3-5-home-5-setting-and-information.jpg": "Настройки / Инфо",
    "st15-cs-hc-3-6-home-6-Honda-Total-Care.jpg": "Honda Total Care",
    "st15-cs-hc-3-7-home-7-Audio-Source.jpg": "Источник аудио",
    "st15-cs-hc-3-7-2-home-7-Audio-Source.jpg": "Источник аудио",
    "st15-cs-hc-3-7-3-home-7-Audio-Source.jpg": "Источник аудио",
    "st15-cs-hc-3-8-home-8-owners-manual.jpg": "Руководство",
    "st15-cs-hc-3-9-home-9-Wi-Fi.jpg": "Wi‑Fi в салоне",
    "st15-cs-hc-3-10-home-10-clock.jpg": "Часы",
    "st15-cs-hc-3-11-home-11-menu-custmize.jpg": "Настройка HOME",
    "st15-cs-hc-3-14-home-14-PM2.5.jpg": "PM2.5",
    "st15-cs-hc-3-15-home-15-multi-view-camera.jpg": "Камеры Multi-View",
    "st15-cs-hc-3-15-2-home-15-multi-view-camera.jpg": "Камера",
}


def font(size: int) -> ImageFont.FreeTypeFont:
    for name in (
        r"C:\Windows\Fonts\segoeui.ttf",
        r"C:\Windows\Fonts\arial.ttf",
        r"C:\Windows\Fonts\tahoma.ttf",
    ):
        p = Path(name)
        if p.is_file():
            return ImageFont.truetype(str(p), size)
    return ImageFont.load_default()


def cover_and_center_text(
    im: Image.Image,
    text: str,
    band_top_ratio: float = 0.68,
    band_bottom_ratio: float = 0.92,
    fill=(230, 240, 255),
) -> Image.Image:
    out = im.copy().convert("RGBA")
    w, h = out.size
    y0, y1 = int(h * band_top_ratio), int(h * band_bottom_ratio)
    # solid black plate — fully hide JP caption
    d0 = ImageDraw.Draw(out)
    d0.rectangle((0, y0, w, y1), fill=(0, 0, 0, 255))
    d2 = ImageDraw.Draw(out)
    size = max(32, w // 16)
    f = font(size)
    bbox = d2.textbbox((0, 0), text, font=f)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    while tw > w * 0.92 and size > 16:
        size -= 2
        f = font(size)
        bbox = d2.textbbox((0, 0), text, font=f)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (w - tw) // 2
    y = y0 + (y1 - y0 - th) // 2
    d2.text((x, y), text, font=f, fill=fill)
    return out.convert("RGB")


def annotate_home(im: Image.Image) -> Image.Image:
    """HOME 2x3 icons — cover JP labels, write RU."""
    out = im.copy().convert("RGBA")
    w, h = out.size
    # Approximate label centers for 2x3 grid (tuned for 1600x947 clicccar crop)
    labels = [
        # (cx_ratio, cy_ratio, text)
        (0.28, 0.48, "Навигация"),
        (0.50, 0.48, "Apple CarPlay"),
        (0.72, 0.48, "Android Auto"),
        (0.28, 0.78, "Телефон"),
        (0.50, 0.78, "Настройки / Инфо"),
        (0.72, 0.78, "Honda Total Care"),
    ]
    overlay = Image.new("RGBA", out.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    bw, bh = int(w * 0.18), int(h * 0.055)
    for cxr, cyr, _ in labels:
        cx, cy = int(w * cxr), int(h * cyr)
        d.rounded_rectangle(
            (cx - bw, cy - bh // 2, cx + bw, cy + bh // 2),
            radius=8,
            fill=(0, 0, 0, 220),
        )
    out = Image.alpha_composite(out, overlay)
    d2 = ImageDraw.Draw(out)
    f = font(max(22, w // 55))
    for cxr, cyr, text in labels:
        cx, cy = int(w * cxr), int(h * cyr)
        bbox = d2.textbbox((0, 0), text, font=f)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        d2.text((cx - tw // 2, cy - th // 2), text, font=f, fill=(235, 245, 255))
    # title strip
    d2.rectangle((int(w * 0.08), int(h * 0.14), int(w * 0.22), int(h * 0.20)), fill=(0, 0, 0, 200))
    d2.text((int(w * 0.09), int(h * 0.15)), "ГЛАВНАЯ", font=font(max(20, w // 60)), fill=(120, 190, 255))
    return out.convert("RGB")


def annotate_settings(im: Image.Image) -> Image.Image:
    out = im.copy().convert("RGBA")
    w, h = out.size
    overlay = Image.new("RGBA", out.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)

    # tabs
    tabs = [
        (0.22, 0.22, 0.38, 0.28, "Настройки"),
        (0.40, 0.22, 0.56, 0.28, "Информация"),
    ]
    items = [
        # left column
        (0.14, 0.34, 0.48, 0.40, "Настройки навигации"),
        (0.14, 0.44, 0.48, 0.50, "Настройки информации"),
        (0.14, 0.54, 0.48, 0.60, "Системные настройки"),
        (0.14, 0.64, 0.48, 0.70, "Громкость"),
        # right column
        (0.52, 0.34, 0.90, 0.40, "Настройки AV"),
        (0.52, 0.44, 0.90, 0.50, "Bluetooth / InterNavi"),
        (0.52, 0.54, 0.90, 0.60, "Настройки iPod"),
    ]
    # hard key 現在地
    items.append((0.58, 0.90, 0.72, 0.96, "Карта (здесь)"))

    for x0, y0, x1, y1, _ in tabs + items:
        d.rounded_rectangle(
            (int(w * x0), int(h * y0), int(w * x1), int(h * y1)),
            radius=6,
            fill=(0, 0, 0, 215),
        )
    out = Image.alpha_composite(out, overlay)
    d2 = ImageDraw.Draw(out)
    f_tab = font(max(22, w // 48))
    f_item = font(max(20, w // 55))
    for x0, y0, x1, y1, text in tabs:
        bbox = d2.textbbox((0, 0), text, font=f_tab)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        cx = int(w * (x0 + x1) / 2)
        cy = int(h * (y0 + y1) / 2)
        d2.text((cx - tw // 2, cy - th // 2), text, font=f_tab, fill=(255, 255, 255))
    for x0, y0, x1, y1, text in items:
        bbox = d2.textbbox((0, 0), text, font=f_item)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        x = int(w * x0) + 12
        cy = int(h * (y0 + y1) / 2)
        d2.text((x, cy - th // 2), text, font=f_item, fill=(235, 245, 255))
    return out.convert("RGB")


def annotate_switch(im: Image.Image) -> Image.Image:
    out = im.copy().convert("RGBA")
    w, h = out.size
    # Cover Japanese callouts with RU (approximate positions from diagram)
    callouts = [
        (0.02, 0.78, 0.12, 0.86, "Микрофон"),
        (0.10, 0.72, 0.28, 0.82, "Открыть\nпанель"),
        (0.22, 0.72, 0.38, 0.82, "Опция"),
        (0.34, 0.72, 0.50, 0.82, "Громкость\n− ＋"),
        (0.48, 0.72, 0.62, 0.82, "AUDIO"),
        (0.58, 0.72, 0.74, 0.82, "Карта\n(здесь)"),
        (0.70, 0.72, 0.84, 0.82, "HOME"),
        (0.82, 0.72, 0.96, 0.82, "Питание\nаудио"),
        (0.90, 0.78, 0.99, 0.86, "Микрофон"),
        (0.20, 0.02, 0.80, 0.08, "Honda CONNECT — экран и кнопки"),
    ]
    # Also cover on-screen JP under icons
    screen_labels = [
        (0.22, 0.48, 0.38, 0.54, "Навигация"),
        (0.40, 0.48, 0.56, 0.54, "CarPlay"),
        (0.58, 0.48, 0.74, 0.54, "Android Auto"),
        (0.22, 0.62, 0.38, 0.68, "Телефон"),
        (0.40, 0.62, 0.56, 0.68, "Настройки"),
        (0.58, 0.62, 0.74, 0.68, "Total Care"),
    ]
    overlay = Image.new("RGBA", out.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    for x0, y0, x1, y1, _ in callouts + screen_labels:
        d.rounded_rectangle(
            (int(w * x0), int(h * y0), int(w * x1), int(h * y1)),
            radius=6,
            fill=(8, 20, 40, 230),
        )
    out = Image.alpha_composite(out, overlay)
    d2 = ImageDraw.Draw(out)
    f = font(max(16, w // 70))
    f_title = font(max(22, w // 55))
    for x0, y0, x1, y1, text in callouts + screen_labels:
        use = f_title if "Honda CONNECT" in text else f
        lines = text.split("\n")
        cy = int(h * (y0 + y1) / 2)
        total_h = 0
        sizes = []
        for line in lines:
            bbox = d2.textbbox((0, 0), line, font=use)
            sizes.append((bbox[2] - bbox[0], bbox[3] - bbox[1]))
            total_h += bbox[3] - bbox[1] + 2
        y = cy - total_h // 2
        cx = int(w * (x0 + x1) / 2)
        for line, (tw, th) in zip(lines, sizes):
            d2.text((cx - tw // 2, y), line, font=use, fill=(180, 220, 255))
            y += th + 2
    return out.convert("RGB")


SETTINGS_SUB = {
    "st15-cs-hc-5-set-and-info.jpg": None,  # special
    "st15-cs-hc-5-2-set-and-info-2-av.jpg": "Настройки AV",
    "st15-cs-hc-5-2-1-set-and-info-2-av-1-sound-setting.jpg": "Звук",
    "st15-cs-hc-5-3-set-and-info-3-info-set.jpg": "Настройки информации",
    "st15-cs-hc-5-3-2-set-and-info-3-info-set-2-phone-set.jpg": "Настройки телефона",
    "st15-cs-hc-5-3-3-set-and-info-3-info-set-3-etc-set.jpg": "Настройки ETC",
    "st15-cs-hc-5-4-set-and-info-4-bluetooth-and-internavi-set.jpg": "Bluetooth / InterNavi",
    "st15-cs-hc-5-4-1-set-and-info-4-bluetooth-and-internavi-set-1-bluetooth.jpg": "Bluetooth",
    "st15-cs-hc-5-5-set-and-info-5-system-setting.jpg": "Системные настройки",
    "st15-cs-hc-5-5-2-set-and-info-5-system-setting-2-hard-key.jpg": "Физические кнопки",
    "st15-cs-hc-5-5-2-2-set-and-info-5-system-setting-2-2-steering-switch.jpg": "Кнопки на руле",
    "st15-cs-hc-5-5-3-set-and-info-5-system-setting-3-clock-set.jpg": "Часы",
    "st15-cs-hc-5-5-5-set-and-info-5-system-setting-5-camera.jpg": "Камера",
    "st15-cs-hc-5-6-set-and-info-6-ipod-setting.jpg": "iPod",
    "st15-cs-hc-5-7-1-set-and-info-7-volume-set-1-system.jpg": "Громкость: система",
    "st15-cs-hc-5-7-2-set-and-info-7-volume-set-2-telephone.jpg": "Громкость: телефон",
    "st15-cs-hc-5-7-3-set-and-info-7-volume-set-3-audio.jpg": "Громкость: аудио",
    "st15-cs-hc-5-7-4-set-and-info-7-volume-set-4-taliking-with-rear-passenger-system.jpg": "Громкость: разговор сзади",
    "st15-cs-hc-6-talking-switch-we.jpg": "Разговор с задним рядом",
    "st15-cs-hc-7-owners-manual.jpg": "Руководство в мониторе",
    "st15-cs-hc-7-2-owners-manual.jpg": "Разделы руководства",
    "st15-cs-hc-7-4-owners-manual.jpg": "Поиск в руководстве",
    "st15-cs-hc-0-main-we.jpg": "Honda CONNECT в салоне",
    "st15-cs-hc-2-2-home.jpg": "HOME — свайп",
}


def banner(im: Image.Image, text: str) -> Image.Image:
    """Top banner with Russian title; keep photo, add clear RU header."""
    out = im.copy().convert("RGB")
    w, h = out.size
    d = ImageDraw.Draw(out)
    bar_h = max(48, h // 14)
    d.rectangle((0, 0, w, bar_h), fill=(10, 18, 28))
    f = font(max(22, w // 40))
    bbox = d.textbbox((0, 0), text, font=f)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    d.text(((w - tw) // 2, (bar_h - th) // 2), text, font=f, fill=(180, 220, 255))
    # also cover bottom JP if present on icon-like screens
    if h > 600 and w < 1400:
        return cover_and_center_text(out, text, 0.78, 0.92)
    return out


def main():
    done = 0
    # HOME
    home = SRC / "st15-cs-hc-2-home.jpg"
    if home.is_file():
        annotate_home(Image.open(home)).save(OUT / "st15-cs-hc-2-home.jpg", quality=90)
        done += 1

    # settings main
    sett = SRC / "st15-cs-hc-5-set-and-info.jpg"
    if sett.is_file():
        annotate_settings(Image.open(sett)).save(OUT / "st15-cs-hc-5-set-and-info.jpg", quality=90)
        done += 1

    # switches
    sw = SRC / "st15-cs-hc-1-honda-connect-switch-we.jpg"
    if sw.is_file():
        annotate_switch(Image.open(sw)).save(OUT / "st15-cs-hc-1-honda-connect-switch-we.jpg", quality=90)
        done += 1
    sw2 = SRC / "st15-cs-hc-1-honda-connect-switch.jpg"
    if sw2.is_file():
        annotate_switch(Image.open(sw2)).save(OUT / "st15-cs-hc-1-honda-connect-switch.jpg", quality=90)
        done += 1

    for name, ru in ICON_RU.items():
        src = SRC / name
        if not src.is_file():
            print("skip", name)
            continue
        cover_and_center_text(Image.open(src), ru).save(OUT / name, quality=90)
        done += 1

    for name, ru in SETTINGS_SUB.items():
        if ru is None:
            continue
        src = SRC / name
        if not src.is_file():
            print("skip", name)
            continue
        if name.startswith("st15-cs-hc-3-") or "home-" in name:
            cover_and_center_text(Image.open(src), ru).save(OUT / name, quality=90)
        else:
            banner(Image.open(src), ru).save(OUT / name, quality=90)
        done += 1

    print("written", done, "->", OUT)


if __name__ == "__main__":
    main()
