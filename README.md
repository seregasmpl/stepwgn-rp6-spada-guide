# Honda STEP WGN RP6 SPADA — справочник (RU)

Офлайн-справочник на русском: приборка / MID, Honda CONNECT, климат, сиденья, руль, лампы. Фото с подписями JP→RU (Honda OM JPN, обзоры Clicccar).

**Версия:** v1.4 · HD-фото · зум по клику · навигация по разделам

## Открыть локально

Откройте [`index.html`](index.html) в браузере (двойной клик или «Open with Live Server»).

Для iPhone без интернета после скачивания репозитория: [`STEPWGN-SPADA-guide-iphone.html`](STEPWGN-SPADA-guide-iphone.html) (один файл, всё внутри).

## Опубликовать на GitHub (ссылка в интернете)

Сайт будет доступен по адресу:

`https://<ваш-логин>.github.io/<имя-репозитория>/`

### 1. Создайте репозиторий на GitHub

1. [github.com/new](https://github.com/new)
2. Имя, например: `stepwgn-rp6-spada-guide`
3. **Public** (для бесплатного Pages) или Private + Pages (платный план)
4. Без README / .gitignore — они уже в этой папке

### 2. Залейте код из этой папки

В PowerShell (путь к папке — ваш):

```powershell
cd "c:\Папки для проги\syepwgn\stepwgn-rp6-spada-guide"
git init
git add .
git commit -m "STEP WGN RP6 SPADA guide v1.4"
git branch -M main
git remote add origin https://github.com/<ВАШ_ЛОГИН>/stepwgn-rp6-spada-guide.git
git push -u origin main
```

Первый push ~100 MB (фото) — может занять несколько минут.

### 3. Включите GitHub Pages

1. Репозиторий → **Settings** → **Pages**
2. **Build and deployment** → Source: **GitHub Actions**
3. После успешного workflow **Deploy GitHub Pages** (вкладка Actions) появится ссылка на сайт

Либо один раз: Actions → **Deploy GitHub Pages** → **Run workflow**.

### 4. Проверка

- Главная: `https://<логин>.github.io/<репо>/`
- iPhone-версия: `https://<логин>.github.io/<репо>/STEPWGN-SPADA-guide-iphone.html`

На телефоне: «Поделиться» → **На экран Домой** (есть `manifest.json` для режима приложения).

## Обновление после правок

```powershell
git add .
git commit -m "описание изменений"
git push
```

Через 1–2 минуты сайт обновится автоматически.

## Сборка и инструменты

| Скрипт | Назначение |
|--------|------------|
| `tools/build-iphone-single-html.py` | Один HTML для офлайн на iPhone |
| `tools/download-max-images.py` | Скачать крупные фото Clicccar |
| `tools/upgrade-html-images.py` | Подставить max-URL в index.html |

```powershell
python tools/build-iphone-single-html.py
```

## Структура

```
index.html              # основной справочник
assets/css, assets/js
assets/img/             # фото (~100 MB)
STEPWGN-SPADA-guide-iphone.html
tools/
```

## Источники и дисклеймер

Материалы основаны на Honda Owners Manual (JPN) и публичных обзорах Clicccar. Неофициальный справочник владельца; Honda / Clicccar не аффилированы. Фото — только для личного пользования; при публичном репозитории учитывайте авторские права источников.

## Лицензия

Тексты перевода и вёрстка — по вашему усмотрению (добавьте `LICENSE` при необходимости). Сторонние изображения принадлежат правообладателям.
