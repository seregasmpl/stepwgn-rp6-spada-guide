import re, urllib.request
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
html = (ROOT / "tmp/clicccar_1313854.html").read_text(encoding="utf-8")
names = sorted(set(re.findall(r"uploads/2023/09/22/(st10[^\"'?]+\.jpg)", html)))
out = ROOT / "assets/img/clicccar/1313854"
out.mkdir(parents=True, exist_ok=True)
for name in names:
    p = out / name
    if p.exists():
        continue
    url = f"https://clicccar.com/uploads/2023/09/22/{name}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        p.write_bytes(r.read())
    print("ok", name)
print("total", len(names), "on disk", len(list(out.glob("*.jpg"))))
