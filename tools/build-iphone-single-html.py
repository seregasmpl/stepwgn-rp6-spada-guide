# -*- coding: utf-8 -*-
"""Build one self-contained HTML for iPhone (inline CSS/JS + base64 images)."""
import base64
import re
from io import BytesIO
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
OUT = ROOT / "STEPWGN-SPADA-guide-iphone.html"
CSS = ROOT / "assets/css/style.css"
JS = ROOT / "assets/js/app.js"

EXTRA_CSS = """
html{-webkit-text-size-adjust:100%}
body{
  padding-bottom:env(safe-area-inset-bottom);
  -webkit-overflow-scrolling:touch;
}
.img-grid{grid-template-columns:repeat(auto-fill,minmax(140px,1fr))}
"""

MAX_EDGE = 1200
JPEG_QUALITY = 82


def resolve_file(rel: str) -> Path | None:
    if not rel.startswith("./assets/"):
        return None
    if not re.search(r"\.(jpe?g|png|webp)$", rel, re.I):
        return None
    fp = ROOT / rel[2:].replace("/", "\\")
    if fp.is_file():
        return fp
    stem = fp.stem
    ext = fp.suffix
    plain = re.sub(r"-\d+x\d+$", "", stem, flags=re.I)
    for cand in [fp.parent / f"{plain}{ext}", fp.parent / f"{plain}.jpg"]:
        if cand.is_file():
            return cand
    return None


def collect_paths(html: str) -> set[str]:
    paths = set()
    for m in re.finditer(r'(?:src|data-full)="(\./assets/[^"]+)"', html):
        paths.add(m.group(1))
    return paths


def image_to_data_uri(path: Path) -> str:
    try:
        from PIL import Image
    except ImportError:
        raw = path.read_bytes()
        mime = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
        b64 = base64.standard_b64encode(raw).decode("ascii")
        return f"data:{mime};base64,{b64}"

    img = Image.open(path)
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
    w, h = img.size
    if max(w, h) > MAX_EDGE:
        ratio = MAX_EDGE / max(w, h)
        img = img.resize((int(w * ratio), int(h * ratio)), Image.Resampling.LANCZOS)
    buf = BytesIO()
    img.save(buf, format="JPEG", quality=JPEG_QUALITY, optimize=True)
    b64 = base64.standard_b64encode(buf.getvalue()).decode("ascii")
    return f"data:image/jpeg;base64,{b64}"


def main():
    html = INDEX.read_text(encoding="utf-8")
    css = CSS.read_text(encoding="utf-8") + EXTRA_CSS
    js = JS.read_text(encoding="utf-8")

    html = re.sub(r'<link[^>]*style\.css[^>]*>\s*', "", html)
    html = re.sub(r'<script[^>]*app\.js[^>]*></script>\s*', "", html)

    body_end = html.rfind("</body>")
    if body_end == -1:
        raise SystemExit("index.html: missing </body>")
    html_body = html[:body_end]
    html_tail = html[body_end:]

    paths = collect_paths(html_body)
    cache: dict[str, str] = {}
    total = 0
    for i, rel in enumerate(sorted(paths), 1):
        fp = resolve_file(rel)
        if not fp:
            print("missing", rel)
            continue
        try:
            uri = image_to_data_uri(fp)
        except Exception:
            print("skip", rel)
            continue
        cache[rel] = uri
        total += len(uri)
        if i % 20 == 0:
            print("embed", i, "/", len(paths))

    for rel, uri in cache.items():
        html_body = html_body.replace(f'"{rel}"', f'"{uri}"')
        html_body = html_body.replace(f"'{rel}'", f"'{uri}'")

    html_body = html_body.replace(
        "Клик по фото — увеличение на весь экран (Esc — закрыть). Офлайн.",
        "Клик по фото — увеличение. Меню: «☰ Разделы». Офлайн.",
    )

    html = html_body
    html = re.sub(
        r"<meta name=\"viewport\"[^>]*>",
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />',
        html,
        count=1,
    )
    if "apple-mobile-web-app" not in html:
        html = html.replace(
            "<head>",
            "<head>\n"
            '  <meta name="apple-mobile-web-app-capable" content="yes" />\n'
            '  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent" />\n',
            1,
        )
    html = re.sub(
        r"<title>[^<]*</title>",
        "<title>STEP WGN RP6 SPADA — справочник (iPhone)</title>",
        html,
        count=1,
    )
    html = html.replace(
        "</head>",
        f"  <style>\n{css}\n  </style>\n</head>",
        1,
    )

    out_html = html + f"  <script>\n{js}\n  </script>\n" + html_tail

    if "</html>" not in out_html or "initPanelRouter" not in out_html:
        raise SystemExit("build validation failed: incomplete HTML")

    OUT.write_text(out_html, encoding="utf-8")
    mb = OUT.stat().st_size / (1024 * 1024)
    print("written", OUT.name, f"{mb:.1f} MB", "images", len(cache), "uri MB", total / 1024 / 1024)


if __name__ == "__main__":
    main()
