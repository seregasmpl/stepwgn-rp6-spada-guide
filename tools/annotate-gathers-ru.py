# -*- coding: utf-8 -*-
"""Annotate ALL Honda CONNECT screenshots with Russian labels."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "assets" / "img" / "clicccar" / "1320797"
OUT = ROOT / "assets" / "img" / "gathers-ru"
OUT.mkdir(parents=True, exist_ok=True)

# Russian title / primary label per file
TITLES: dict[str, str] = {
    "st15-cs-hc-0-main-we.jpg": "Honda CONNECT в салоне",
    "st15-cs-hc-1-honda-connect-switch-we.jpg": "Экран и кнопки",
    "st15-cs-hc-1-honda-connect-switch.jpg": "Экран и кнопки",
    "st15-cs-hc-2-home.jpg": "HOME — главная",
    "st15-cs-hc-2-2-home.jpg": "HOME — свайп",
    "st15-cs-hc-3-home-1-navi-menu.jpg": "Меню навигации",
    "st15-cs-hc-3-2-home-2-Apple-CarPlay.jpg": "Apple CarPlay",
    "st15-cs-hc-3-3-home-3-Android-Auto.jpg": "Android Auto",
    "st15-cs-hc-3-4-home-4-telephone.jpg": "Телефон",
    "st15-cs-hc-3-4-2-home-4-telephone.jpg": "Звонок",
    "st15-cs-hc-3-5-home-5-setting-and-information.jpg": "Настройки / Инфо",
    "st15-cs-hc-3-6-home-6-Honda-Total-Care.jpg": "Honda Total Care",
    "st15-cs-hc-3-7-home-7-Audio-Source.jpg": "Источник аудио",
    "st15-cs-hc-3-7-2-home-7-Audio-Source.jpg": "Источники: радио / TV / USB…",
    "st15-cs-hc-3-7-3-home-7-Audio-Source.jpg": "Источники аудио",
    "st15-cs-hc-3-8-home-8-owners-manual.jpg": "Руководство",
    "st15-cs-hc-3-8-2-home-8-owners-manual.jpg": "Руководство: оглавление",
    "st15-cs-hc-3-8-3-home-8-owners-manual.jpg": "Руководство: разделы",
    "st15-cs-hc-3-8-4-home-8-owners-manual.jpg": "Руководство",
    "st15-cs-hc-3-8-5-home-8-owners-manual.jpg": "Руководство: текст",
    "st15-cs-hc-3-8-6-home-8-owners-manual.jpg": "Руководство: лампы",
    "st15-cs-hc-3-8-7-home-8-owners-manual.jpg": "Руководство",
    "st15-cs-hc-3-8-8-home-8-owners-manual.jpg": "Руководство",
    "st15-cs-hc-3-9-home-9-Wi-Fi.jpg": "Wi‑Fi в салоне",
    "st15-cs-hc-3-9-2-home-9-Wi-Fi.jpg": "Настройка Wi‑Fi",
    "st15-cs-hc-3-10-home-10-clock.jpg": "Часы",
    "st15-cs-hc-3-10-2-home-10-clock.jpg": "Часы: аналог",
    "st15-cs-hc-3-10-4-home-10-clock.jpg": "Часы: цифры",
    "st15-cs-hc-3-10-5-home-10-clock.jpg": "Настройка часов",
    "st15-cs-hc-3-11-home-11-menu-custmize.jpg": "Правка меню HOME",
    "st15-cs-hc-3-11-2-home-11-menu-custmize.jpg": "HOME: 3 иконки",
    "st15-cs-hc-3-11-3-home-11-menu-custmize.jpg": "HOME: 4 иконки",
    "st15-cs-hc-3-11-4-home-11-menu-custmize.jpg": "HOME: 5 иконок",
    "st15-cs-hc-3-11-5-home-11-menu-custmize.jpg": "HOME: 6 иконок",
    "st15-cs-hc-3-11-6-home-11-menu-custmize.jpg": "HOME: 7 иконок",
    "st15-cs-hc-3-11-7-home-11-menu-custmize.jpg": "HOME: 8 иконок",
    "st15-cs-hc-3-14-home-14-PM2.5.jpg": "PM2.5",
    "st15-cs-hc-3-14-2-home-14-PM2.5.jpg": "PM2.5: уровень",
    "st15-cs-hc-3-14-3-home-14-PM2.5.jpg": "PM2.5: очистка OFF",
    "st15-cs-hc-3-14-4-home-14-PM2.5.jpg": "PM2.5: 1 ступень",
    "st15-cs-hc-3-14-5-home-14-PM2.5.jpg": "PM2.5: 2 ступень",
    "st15-cs-hc-3-14-6-home-14-PM2.5.jpg": "PM2.5: 3 ступень",
    "st15-cs-hc-3-14-7-home-14-PM2.5.jpg": "PM2.5",
    "st15-cs-hc-3-15-home-15-multi-view-camera.jpg": "Камеры Multi-View",
    "st15-cs-hc-3-15-2-home-15-multi-view-camera.jpg": "Камера",
    "st15-cs-hc-5-set-and-info.jpg": "Настройки / Информация",
    "st15-cs-hc-5-2-set-and-info-2-av.jpg": "Настройки AV",
    "st15-cs-hc-5-2-1-set-and-info-2-av-1-sound-setting.jpg": "Звук (эквалайзер)",
    "st15-cs-hc-5-2-1-2-set-and-info-2-av-1-2-sound-setting.jpg": "Звук: баланс / тон",
    "st15-cs-hc-5-2-2-set-and-info-2-av-2-recording-method.jpg": "Запись на Music Rack",
    "st15-cs-hc-5-2-3-set-and-info-2-av-3-dvd-initial-setting.jpg": "Настройки DVD",
    "st15-cs-hc-5-3-set-and-info-3-info-set.jpg": "Настройки информации",
    "st15-cs-hc-5-3-2-set-and-info-3-info-set-2-phone-set.jpg": "Настройки телефона",
    "st15-cs-hc-5-3-3-set-and-info-3-info-set-3-etc-set.jpg": "Настройки ETC",
    "st15-cs-hc-5-4-set-and-info-4-bluetooth-and-internavi-set.jpg": "Bluetooth / InterNavi",
    "st15-cs-hc-5-4-1-set-and-info-4-bluetooth-and-internavi-set-1-bluetooth.jpg": "Bluetooth",
    "st15-cs-hc-5-4-2-set-and-info-4-bluetooth-and-internavi-set-2-internavi.jpg": "InterNavi",
    "st15-cs-hc-5-5-set-and-info-5-system-setting.jpg": "Системные настройки",
    "st15-cs-hc-5-5-1-set-and-info-5-system-setting-1-security.jpg": "Безопасность",
    "st15-cs-hc-5-5-2-set-and-info-5-system-setting-2-hard-key.jpg": "Физические кнопки",
    "st15-cs-hc-5-5-2-1-set-and-info-5-system-setting-2-2-option-button.jpg": "Кнопка «Опция»",
    "st15-cs-hc-5-5-2-2-set-and-info-5-system-setting-2-2-steering-switch.jpg": "Кнопки на руле",
    "st15-cs-hc-5-5-3-set-and-info-5-system-setting-3-clock-set.jpg": "Часы",
    "st15-cs-hc-5-5-4-set-and-info-5-system-setting-4-boot-picture-change.jpg": "Экран запуска",
    "st15-cs-hc-5-5-5-set-and-info-5-system-setting-5-camera.jpg": "Камера Multi-View",
    "st15-cs-hc-5-5-6-set-and-info-5-system-setting-6-parking-sensor.jpg": "Парктроник",
    "st15-cs-hc-5-5-7-set-and-info-5-system-setting-7-system-information.jpg": "Информация о системе",
    "st15-cs-hc-5-5-7-2-set-and-info-5-system-setting-7-system-information-2.jpg": "Сертификаты",
    "st15-cs-hc-5-5-7-3-set-and-info-5-system-setting-7-system-information-3.jpg": "Доверенные сертификаты",
    "st15-cs-hc-5-5-7-4-set-and-info-5-system-setting-7-system-information-4.jpg": "Версия ПО",
    "st15-cs-hc-5-5-7-5-set-and-info-5-system-setting-7-system-information-5.jpg": "Лицензии",
    "st15-cs-hc-5-5-9-set-and-info-5-system-setting-9-memory-reset.jpg": "Сброс памяти",
    "st15-cs-hc-5-6-set-and-info-6-ipod-setting.jpg": "Настройки iPod",
    "st15-cs-hc-5-7-1-set-and-info-7-volume-set-1-system.jpg": "Громкость: система / нави",
    "st15-cs-hc-5-7-2-set-and-info-7-volume-set-2-telephone.jpg": "Громкость: телефон",
    "st15-cs-hc-5-7-3-set-and-info-7-volume-set-3-audio.jpg": "Громкость: аудио",
    "st15-cs-hc-5-7-4-set-and-info-7-volume-set-4-taliking-with-rear-passenger-system.jpg": "Громкость: разговор сзади",
    "st15-cs-hc-6-talking-switch-we.jpg": "Разговор с задним рядом",
    "st15-cs-hc-7-owners-manual.jpg": "Руководство в мониторе",
    "st15-cs-hc-7-2-owners-manual.jpg": "Оглавление руководства",
    "st15-cs-hc-7-3-owners-manual.jpg": "Руководство: вождение",
    "st15-cs-hc-7-4-owners-manual.jpg": "Руководство: поиск",
    "st15-cs-hc-7-5-owners-manual.jpg": "Руководство: свет",
    "st15-cs-hc-7-6-owners-manual.jpg": "Руководство: ACL",
    "st15-cs-hc-7-7-owners-manual.jpg": "Руководство",
    "st15-cs-hc-7-8-owners-manual.jpg": "Руководство",
    "st15-cs-hc-7-9-owners-manual.jpg": "Руководство",
    "st15-cs-hc-7-10-owners-manual.jpg": "Руководство: лампы",
    "st15-cs-hc-7-11-owners-manual.jpg": "Руководство: лампы",
}

# List menus: (y_ratio_start, y_ratio_end, russian lines)
LIST_MENUS: dict[str, list[tuple[float, float, str]]] = {
    "st15-cs-hc-5-5-set-and-info-5-system-setting.jpg": [
        (0.18, 0.26, "Система"),
        (0.28, 0.35, "Безопасность"),
        (0.36, 0.43, "Физические кнопки"),
        (0.44, 0.51, "Часы"),
        (0.52, 0.59, "Экран запуска"),
        (0.60, 0.67, "Камера Multi-View"),
        (0.68, 0.75, "Парктроник"),
        (0.76, 0.83, "Информация о системе"),
    ],
    "st15-cs-hc-5-5-2-set-and-info-5-system-setting-2-hard-key.jpg": [
        (0.30, 0.40, "Физические кнопки"),
        (0.42, 0.52, "Кнопка «Опция»"),
        (0.54, 0.64, "Кнопки на руле"),
    ],
    "st15-cs-hc-5-2-set-and-info-2-av.jpg": [
        (0.28, 0.38, "Звук (Sound Settings)"),
        (0.40, 0.50, "Способ записи (Music Rack)"),
        (0.52, 0.62, "Настройки DVD"),
    ],
    "st15-cs-hc-5-3-set-and-info-3-info-set.jpg": [
        (0.28, 0.38, "Редактирование номеров"),
        (0.40, 0.50, "Настройки телефона"),
        (0.52, 0.62, "Настройки ETC"),
    ],
    "st15-cs-hc-5-4-set-and-info-4-bluetooth-and-internavi-set.jpg": [
        (0.30, 0.42, "Bluetooth"),
        (0.44, 0.56, "InterNavi"),
    ],
    "st15-cs-hc-5-3-2-set-and-info-3-info-set-2-phone-set.jpg": [
        (0.26, 0.34, "Автоответ"),
        (0.36, 0.44, "Синхронизация телефонной книги"),
        (0.46, 0.54, "Синхронизация истории"),
        (0.56, 0.64, "Показ истории"),
    ],
    "st15-cs-hc-5-3-3-set-and-info-3-info-set-3-etc-set.jpg": [
        (0.16, 0.22, "Настройки ETC"),
        (0.24, 0.30, "Иконка «карта вставлена»"),
        (0.31, 0.37, "Зуммер блока ETC"),
        (0.38, 0.44, "Голосовые подсказки"),
        (0.45, 0.51, "Предупреждение: карта забыта"),
        (0.52, 0.58, "Срок действия карты"),
        (0.59, 0.65, "Время показа поверх экрана"),
        (0.66, 0.72, "Громкость блока ETC"),
    ],
    "st15-cs-hc-5-5-1-set-and-info-5-system-setting-1-security.jpg": [
        (0.28, 0.38, "Пароль / блокировка"),
        (0.40, 0.50, "Мигание индикатора при выкл."),
    ],
    "st15-cs-hc-5-5-7-set-and-info-5-system-setting-7-system-information.jpg": [
        (0.22, 0.30, "Информация о системе"),
        (0.32, 0.40, "Сертификаты"),
        (0.42, 0.50, "Версия ПО"),
        (0.52, 0.60, "Лицензии"),
        (0.62, 0.70, "Приложения и уведомления"),
    ],
    "st15-cs-hc-5-7-1-set-and-info-7-volume-set-1-system.jpg": [
        (0.26, 0.34, "Голос навигации"),
        (0.36, 0.44, "Звук операций"),
        (0.46, 0.54, "Громкость от скорости"),
    ],
    "st15-cs-hc-5-7-2-set-and-info-7-volume-set-2-telephone.jpg": [
        (0.26, 0.34, "Громкость звонка"),
        (0.36, 0.44, "Громкость передачи"),
        (0.46, 0.54, "Громкость приёма"),
        (0.56, 0.64, "От скорости"),
    ],
    "st15-cs-hc-5-7-3-set-and-info-7-volume-set-3-audio.jpg": [
        (0.28, 0.38, "Громкость аудио"),
        (0.40, 0.50, "От скорости"),
    ],
    "st15-cs-hc-5-7-4-set-and-info-7-volume-set-4-taliking-with-rear-passenger-system.jpg": [
        (0.28, 0.40, "Громкость разговора сзади"),
    ],
}


def font(size: int) -> ImageFont.FreeTypeFont:
    for name in (
        r"C:\Windows\Fonts\segoeui.ttf",
        r"C:\Windows\Fonts\arial.ttf",
        r"C:\Windows\Fonts\tahoma.ttf",
    ):
        if Path(name).is_file():
            return ImageFont.truetype(name, size)
    return ImageFont.load_default()


def add_banner(im: Image.Image, text: str) -> Image.Image:
    out = im.convert("RGB")
    w, h = out.size
    d = ImageDraw.Draw(out)
    bar = max(44, h // 16)
    d.rectangle((0, 0, w, bar), fill=(8, 16, 28))
    f = font(max(20, min(36, w // 38)))
    bbox = d.textbbox((0, 0), text, font=f)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    d.text(((w - tw) // 2, (bar - th) // 2), text, font=f, fill=(170, 210, 255))
    return out


def cover_icon_caption(im: Image.Image, text: str) -> Image.Image:
    out = im.convert("RGBA")
    w, h = out.size
    y0, y1 = int(h * 0.66), int(h * 0.93)
    d = ImageDraw.Draw(out)
    d.rectangle((0, y0, w, y1), fill=(0, 0, 0, 255))
    f = font(max(30, w // 15))
    bbox = d.textbbox((0, 0), text, font=f)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    while tw > w * 0.92 and f.size > 16:
        f = font(f.size - 2)
        bbox = d.textbbox((0, 0), text, font=f)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    d.text(((w - tw) // 2, y0 + (y1 - y0 - th) // 2), text, font=f, fill=(235, 245, 255))
    return out.convert("RGB")


def overlay_list(im: Image.Image, rows: list[tuple[float, float, str]]) -> Image.Image:
    out = im.convert("RGBA")
    w, h = out.size
    d = ImageDraw.Draw(out)
    f = font(max(22, w // 42))
    for y0r, y1r, text in rows:
        y0, y1 = int(h * y0r), int(h * y1r)
        d.rectangle((int(w * 0.06), y0, int(w * 0.78), y1), fill=(0, 0, 0, 245))
        bbox = d.textbbox((0, 0), text, font=f)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        d.text((int(w * 0.10), y0 + (y1 - y0 - th) // 2), text, font=f, fill=(240, 248, 255))
    # 現在地 button
    d.rectangle((int(w * 0.55), int(h * 0.90), int(w * 0.72), int(h * 0.97)), fill=(0, 0, 0, 230))
    t = "Карта"
    bbox = d.textbbox((0, 0), t, font=font(max(18, w // 55)))
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    d.text((int(w * 0.635) - tw // 2, int(h * 0.935) - th // 2), t, font=font(max(18, w // 55)), fill=(120, 190, 255))
    return out.convert("RGB")


def annotate_home(im: Image.Image) -> Image.Image:
    out = im.convert("RGBA")
    w, h = out.size
    labels = [
        (0.28, 0.48, "Навигация"),
        (0.50, 0.48, "CarPlay"),
        (0.72, 0.48, "Android Auto"),
        (0.28, 0.78, "Телефон"),
        (0.50, 0.78, "Настройки"),
        (0.72, 0.78, "Total Care"),
    ]
    d = ImageDraw.Draw(out)
    bw, bh = int(w * 0.15), int(h * 0.055)
    f = font(max(18, w // 58))
    for cxr, cyr, text in labels:
        cx, cy = int(w * cxr), int(h * cyr)
        d.rounded_rectangle((cx - bw, cy - bh // 2, cx + bw, cy + bh // 2), radius=8, fill=(0, 0, 0, 230))
        bbox = d.textbbox((0, 0), text, font=f)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        d.text((cx - tw // 2, cy - th // 2), text, font=f, fill=(235, 245, 255))
    out = add_banner(out.convert("RGB"), "HOME — главная")
    return out


def annotate_settings_root(im: Image.Image) -> Image.Image:
    out = im.convert("RGBA")
    w, h = out.size
    d = ImageDraw.Draw(out)
    # Cover JP row text (left/right columns) with RU labels aligned to real rows
    blocks = [
        (0.20, 0.175, 0.42, 0.245, "Настройки"),
        (0.44, 0.175, 0.66, 0.245, "Информация"),
        (0.18, 0.30, 0.48, 0.37, "Настройки навигации"),
        (0.18, 0.40, 0.48, 0.47, "Настройки информации"),
        (0.18, 0.50, 0.48, 0.57, "Системные настройки"),
        (0.18, 0.60, 0.48, 0.67, "Громкость"),
        (0.52, 0.30, 0.90, 0.37, "Настройки AV"),
        (0.52, 0.40, 0.90, 0.47, "Bluetooth / InterNavi"),
        (0.52, 0.50, 0.90, 0.57, "Настройки iPod"),
        (0.58, 0.88, 0.74, 0.95, "Карта"),
    ]
    f = font(max(18, w // 52))
    for x0, y0, x1, y1, text in blocks:
        d.rounded_rectangle((int(w * x0), int(h * y0), int(w * x1), int(h * y1)), radius=6, fill=(0, 0, 0, 235))
        bbox = d.textbbox((0, 0), text, font=f)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        cx = int(w * (x0 + x1) / 2)
        cy = int(h * (y0 + y1) / 2)
        d.text((cx - tw // 2, cy - th // 2), text, font=f, fill=(240, 248, 255))
    return add_banner(out.convert("RGB"), "Настройки / Информация")


def annotate_switch(im: Image.Image) -> Image.Image:
    out = im.convert("RGBA")
    w, h = out.size
    d = ImageDraw.Draw(out)
    callouts = [
        (0.02, 0.78, 0.12, 0.86, "Микрофон"),
        (0.10, 0.70, 0.26, 0.82, "Открыть панель"),
        (0.24, 0.70, 0.38, 0.82, "Опция"),
        (0.36, 0.70, 0.50, 0.82, "Громкость −＋"),
        (0.50, 0.70, 0.62, 0.82, "AUDIO"),
        (0.60, 0.70, 0.74, 0.82, "Карта"),
        (0.72, 0.70, 0.84, 0.82, "HOME"),
        (0.84, 0.70, 0.98, 0.82, "Питание аудио"),
        (0.22, 0.46, 0.38, 0.54, "Навигация"),
        (0.40, 0.46, 0.56, 0.54, "CarPlay"),
        (0.58, 0.46, 0.74, 0.54, "Android Auto"),
        (0.22, 0.60, 0.38, 0.68, "Телефон"),
        (0.40, 0.60, 0.56, 0.68, "Настройки"),
        (0.58, 0.60, 0.74, 0.68, "Total Care"),
    ]
    f = font(max(16, w // 70))
    for x0, y0, x1, y1, text in callouts:
        d.rounded_rectangle((int(w * x0), int(h * y0), int(w * x1), int(h * y1)), radius=6, fill=(8, 20, 40, 235))
        bbox = d.textbbox((0, 0), text, font=f)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        cx = int(w * (x0 + x1) / 2)
        cy = int(h * (y0 + y1) / 2)
        d.text((cx - tw // 2, cy - th // 2), text, font=f, fill=(180, 220, 255))
    return add_banner(out.convert("RGB"), "Экран и кнопки")


def annotate_audio_sources(im: Image.Image) -> Image.Image:
    out = im.convert("RGBA")
    w, h = out.size
    d = ImageDraw.Draw(out)
    labels = [
        (0.28, 0.48, "DVD / CD"),
        (0.50, 0.48, "Радио"),
        (0.72, 0.48, "ТВ"),
        (0.28, 0.72, "Music Rack"),
        (0.50, 0.72, "SD"),
        (0.72, 0.72, "USB"),
        (0.58, 0.92, "Карта"),
    ]
    f = font(max(20, w // 50))
    for cxr, cyr, text in labels:
        cx, cy = int(w * cxr), int(h * cyr)
        bw = int(w * 0.12)
        bh = int(h * 0.05)
        d.rounded_rectangle((cx - bw, cy - bh // 2, cx + bw, cy + bh // 2), radius=6, fill=(0, 0, 0, 230))
        bbox = d.textbbox((0, 0), text, font=f)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        d.text((cx - tw // 2, cy - th // 2), text, font=f, fill=(235, 245, 255))
    return add_banner(out.convert("RGB"), "Источники аудио")


def process(name: str, out_dir: Path) -> None:
    import io

    src = SRC / name
    if not src.is_file():
        return
    with Image.open(src) as im:
        im.load()
        title = TITLES.get(name, name.replace(".jpg", ""))

        if name == "st15-cs-hc-2-home.jpg":
            out = annotate_home(im)
        elif name == "st15-cs-hc-5-set-and-info.jpg":
            out = annotate_settings_root(im)
        elif "honda-connect-switch" in name:
            out = annotate_switch(im)
        elif name == "st15-cs-hc-3-7-2-home-7-Audio-Source.jpg":
            out = annotate_audio_sources(im)
        elif name in LIST_MENUS:
            out = overlay_list(im, LIST_MENUS[name])
            out = add_banner(out, title)
        elif "-home-" in name or name.startswith("st15-cs-hc-3-"):
            out = cover_icon_caption(im, title)
            out = add_banner(out, title)
        else:
            out = add_banner(im, title)

        buf = io.BytesIO()
        out.convert("RGB").save(buf, format="JPEG", quality=90)
        data = buf.getvalue()

    (out_dir / name).write_bytes(data)


def main():
    import shutil
    import tempfile

    names = sorted(
        p.name
        for p in SRC.glob("st15-cs-hc*.jpg")
        if not any(x in p.name for x in ("-200x", "-380x", "-800x"))
    )
    tmp = Path(tempfile.mkdtemp(prefix="gathers-ru-"))
    try:
        for n in names:
            process(n, tmp)
        OUT.mkdir(parents=True, exist_ok=True)
        for n in names:
            shutil.copy2(tmp / n, OUT / n)
        print("done", len(names))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
