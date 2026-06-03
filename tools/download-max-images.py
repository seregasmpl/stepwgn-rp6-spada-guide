# -*- coding: utf-8 -*-
import json
import re
import urllib.request
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[1]
TMP = ROOT / "tmp"
ASSETS = ROOT / "assets" / "img" / "clicccar"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

URL_RE = re.compile(
    r"https://clicccar\.com/uploads/(\d{4}/\d{2}/\d{2})/(st[^\"'?]+\.(?:jpg|jpeg|png|webp))",
    re.I,
)

# tmp filename -> article folder
ARTICLE_BY_TMP = {
    "clicccar_1312122.html": "1312122",
    "clicccar_1313854.html": "1313854",
    "clicccar_1315602.html": "1315602",
    "clicccar_1317716.html": "1317716",
    "clicccar_1320797.html": "1320797",
    "clicccar_1307852.html": "1307852",
    "clicccar_1309393.html": "1309393",
}


def base_key(filename: str) -> str:
    name = filename.rsplit(".", 1)[0]
    m = re.match(r"^(.+?)(?:-\d+x\d+)?$", name, re.I)
    return m.group(1) if m else name


def pixel_area(filename: str) -> int:
    m = re.search(r"-(\d+)x(\d+)\.", filename, re.I)
    return int(m.group(1)) * int(m.group(2)) if m else 99_000_000


def collect_urls():
    urls: set[tuple[str, str, str]] = set()  # date_path, fname, article
    for html in TMP.glob("clicccar_*.html"):
        article = ARTICLE_BY_TMP.get(html.name, html.stem.replace("clicccar_", ""))
        text = html.read_text(encoding="utf-8", errors="ignore")
        for date_path, fname in URL_RE.findall(text):
            urls.add((date_path, fname.split("?")[0], article))

    # plain originals (st5-main.jpg)
    for html in TMP.glob("clicccar_*.html"):
        article = ARTICLE_BY_TMP.get(html.name, html.stem.replace("clicccar_", ""))
        text = html.read_text(encoding="utf-8", errors="ignore")
        for date_path, fname in URL_RE.findall(text):
            ext = fname.rsplit(".", 1)[-1]
            plain = f"{base_key(fname)}.{ext}"
            if plain != fname:
                urls.add((date_path, plain, article))
    return urls


def download_one(date_path: str, fname: str, article: str) -> bool:
    out_dir = ASSETS / article
    out_dir.mkdir(parents=True, exist_ok=True)
    dest = out_dir / fname
    if dest.exists() and dest.stat().st_size > 800:
        return True
    url = f"https://clicccar.com/uploads/{date_path}/{fname}"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            data = r.read()
        if len(data) < 500:
            return False
        dest.write_bytes(data)
        return True
    except Exception:
        return False


def build_manifest():
    manifest = {}
    for d in ASSETS.iterdir():
        if not d.is_dir():
            continue
        best: dict[str, tuple[int, str]] = {}
        for f in d.iterdir():
            if f.suffix.lower() not in {".jpg", ".jpeg", ".png", ".webp"}:
                continue
            b = base_key(f.name)
            area = pixel_area(f.name)
            rel = f.relative_to(ROOT).as_posix()
            if b not in best or area > best[b][0]:
                best[b] = (area, rel)
        for b, (_, rel) in best.items():
            manifest[f"{d.name}/{b}"] = rel
    return manifest


def main():
    urls = collect_urls()
    print("urls to fetch:", len(urls))
    ok = fail = 0
    for date_path, fname, article in sorted(urls):
        if download_one(date_path, fname, article):
            ok += 1
        else:
            fail += 1
    manifest = build_manifest()
    (ROOT / "tools" / "image-manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print("ok", ok, "fail", fail, "manifest", len(manifest))


if __name__ == "__main__":
    main()
