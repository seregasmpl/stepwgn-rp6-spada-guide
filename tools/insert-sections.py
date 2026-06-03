from pathlib import Path

root = Path(__file__).resolve().parents[1]
idx_path = root / "index.html"
idx = idx_path.read_text(encoding="utf-8")
snip = (root / "tools/new-sections-snippet.html").read_text(encoding="utf-8")
marker = '      <section id="cameras-multiview"'
if snip.strip() not in idx:
    idx = idx.replace(marker, snip + marker, 1)
    idx_path.write_text(idx, encoding="utf-8")
    print("inserted")
else:
    print("skip")
