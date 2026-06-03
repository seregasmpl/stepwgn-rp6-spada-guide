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

IPHONE_CSS = """
/* iPhone / mobile */
html{-webkit-text-size-adjust:100%}
body{
  padding-bottom:env(safe-area-inset-bottom);
  -webkit-overflow-scrolling:touch;
}
header{padding-top:env(safe-area-inset-top)}
.wrap{padding:12px;padding-left:max(12px,env(safe-area-inset-left));padding-right:max(12px,env(safe-area-inset-right))}
.title h1{font-size:16px;line-height:1.35}
.nav-toggle{
  display:none;
  width:100%;
  margin-bottom:8px;
  padding:12px 14px;
  font-size:15px;
  font-weight:600;
  border:1px solid var(--border);
  border-radius:12px;
  background:rgba(102,179,255,.12);
  color:var(--text);
  cursor:pointer;
}
@media (max-width: 980px){
  :root{--header-h:56px}
  .layout{display:block;min-height:auto}
  .nav-toggle{display:block}
  .nav{
    position:fixed;
    left:0;right:0;bottom:0;
    top:auto;
    max-height:min(70vh,520px);
    z-index:50;
    border-radius:16px 16px 0 0;
    transform:translateY(110%);
    transition:transform .25s ease;
    box-shadow:0 -8px 32px rgba(0,0,0,.45);
    padding-bottom:max(12px,env(safe-area-inset-bottom));
  }
  .nav.is-open{transform:translateY(0)}
  .nav-backdrop{
    display:none;
    position:fixed;inset:0;
    background:rgba(0,0,0,.5);
    z-index:49;
  }
  .nav-backdrop.is-open{display:block}
  .content-col{
    position:static;
    max-height:none;
    min-height:calc(100vh - var(--header-h) - 8px);
  }
  .main-scroll{overflow:visible;min-height:0}
  .panel-btn{
    min-width:48px;min-height:48px;
    font-size:20px;
  }
  .nav a{padding:12px 12px;font-size:15px}
  .nav input{font-size:16px;padding:12px}
  .table{display:block;overflow-x:auto;-webkit-overflow-scrolling:touch}
  .table th,.table td{font-size:13px;padding:8px}
  .img-grid{grid-template-columns:repeat(auto-fill,minmax(140px,1fr))}
  .lightbox{padding:max(12px,env(safe-area-inset-top)) 12px max(12px,env(safe-area-inset-bottom))}
  .lightbox-close{top:max(12px,env(safe-area-inset-top));right:12px;min-width:48px;min-height:48px}
  .lightbox img{max-width:100vw;max-height:85vh}
  .nav-foot{display:none}
}
"""

IPHONE_JS = """
function initMobileNav(){
  const nav=document.querySelector('.nav');
  if(!nav) return;
  let btn=document.querySelector('[data-nav-toggle]');
  let backdrop=document.querySelector('.nav-backdrop');
  if(!btn){
    btn=document.createElement('button');
    btn.type='button';
    btn.className='nav-toggle';
    btn.setAttribute('data-nav-toggle','');
    btn.textContent='☰ Разделы';
    nav.parentNode.insertBefore(btn,nav);
  }
  if(!backdrop){
    backdrop=document.createElement('div');
    backdrop.className='nav-backdrop';
    backdrop.setAttribute('data-nav-backdrop','');
    document.body.appendChild(backdrop);
  }
  const close=()=>{nav.classList.remove('is-open');backdrop.classList.remove('is-open');};
  const open=()=>{nav.classList.add('is-open');backdrop.classList.add('is-open');};
  btn.onclick=()=>nav.classList.contains('is-open')?close():open();
  backdrop.onclick=close;
  nav.addEventListener('click',e=>{
    if(e.target.closest('[data-nav-item]')) close();
  });
}
document.addEventListener('DOMContentLoaded',()=>{initMobileNav();});
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
    # try without -200xNNN in name
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
    css = CSS.read_text(encoding="utf-8") + IPHONE_CSS
    js = JS.read_text(encoding="utf-8") + IPHONE_JS

    html = re.sub(r'<link[^>]*style\.css[^>]*>\s*', "", html)
    html = re.sub(r'<script[^>]*app\.js[^>]*></script>\s*', "", html)

    paths = collect_paths(html)
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
        html = html.replace(f'"{rel}"', f'"{uri}"')
        html = html.replace(f"'{rel}'", f"'{uri}'")

    html = html.replace(
        "v1.4</span> <span class=\"muted\">офлайн · HD · зум</span>",
        "iPhone</span> <span class=\"muted\">один файл · офлайн</span>",
    )
    html = html.replace(
        '<div class="muted">Файл: <span class="kbd">stepwgn-rp6-spada-guide/index.html</span></div>',
        '<div class="muted">Файлы → откройте в Safari</div>',
    )
    html = html.replace(
        "Клик по фото — увеличение на весь экран (Esc — закрыть). Офлайн.",
        "Клик по фото — увеличение. Меню: кнопка «Разделы» внизу. Офлайн.",
    )

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
    html = html.replace(
        "</body>",
        f"  <script>\n{js}\n  </script>\n</body>",
        1,
    )

    OUT.write_text(html, encoding="utf-8")
    mb = OUT.stat().st_size / (1024 * 1024)
    print("written", OUT.name, f"{mb:.1f} MB", "images", len(cache), "uri MB", total / 1024 / 1024)


if __name__ == "__main__":
    main()
