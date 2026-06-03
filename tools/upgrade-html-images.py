# -*- coding: utf-8 -*-
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
MANIFEST_PATH = ROOT / "tools" / "image-manifest.json"

IMG_RE = re.compile(
    r"<img\s+([\s\S]*?)(?:\s*/>|>)",
    re.I,
)


def base_key_from_src(src: str) -> str | None:
    m = re.search(r"clicccar/(\d+)/([^\"?]+)$", src)
    if not m:
        return None
    article, fname = m.group(1), m.group(2)
    stem = re.sub(r"-\d+x\d+(?=\.\w+$)", "", fname, flags=re.I)
    stem = re.sub(r"\.\w+$", "", stem)
    return f"{article}/{stem}"


def best_path(manifest: dict, src: str) -> str:
    key = base_key_from_src(src)
    if key and key in manifest:
        return "./" + manifest[key]
    return src


def parse_src(attrs: str) -> str | None:
    m = re.search(r'\bsrc="([^"]+)"', attrs, re.I)
    return m.group(1) if m else None


def set_src(attrs: str, src: str) -> str:
    if re.search(r'\bsrc="', attrs, re.I):
        return re.sub(r'\bsrc="[^"]*"', f'src="{src}"', attrs, count=1, flags=re.I)
    return f'src="{src}" ' + attrs


def patch_attrs(attrs: str, full_src: str) -> str:
    attrs = re.sub(r'\s*/\s*$', '', attrs.strip())
    attrs = re.sub(r'\bclass="[^"]*"', '', attrs)
    attrs = re.sub(r'\bdata-full="[^"]*"', '', attrs)
    attrs = re.sub(r'\bloading="[^"]*"', '', attrs)
    attrs = attrs.strip()
    if attrs and not attrs.endswith(" "):
        attrs += " "
    attrs += 'class="zoomable" '
    attrs += f'data-full="{full_src}" loading="lazy"'
    return attrs


def main():
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    html = INDEX.read_text(encoding="utf-8")
    n = 0

    def repl(m):
        nonlocal n
        attrs = m.group(1).strip()
        src = parse_src(attrs)
        if not src or "clicccar" not in src:
            return m.group(0)
        if "/assets/img/" in src and "warning" in src:
            return m.group(0)
        full = best_path(manifest, src)
        attrs = set_src(attrs, full)
        attrs = patch_attrs(attrs, full)
        n += 1
        return f"<img {attrs}>"

    html = IMG_RE.sub(repl, html)
    html = re.sub(r"v1\.3", "v1.4", html)
    INDEX.write_text(html, encoding="utf-8")
    print("images upgraded:", n)


if __name__ == "__main__":
    main()
