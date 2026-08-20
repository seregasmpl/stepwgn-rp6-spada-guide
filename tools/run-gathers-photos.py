# -*- coding: utf-8 -*-
from pathlib import Path
import re
import subprocess
import sys

root = Path(__file__).resolve().parents[1]
subprocess.check_call([sys.executable, str(root / "tools" / "inject-gathers-photos.py")], cwd=root)
subprocess.check_call([sys.executable, str(root / "tools" / "build-gathers-site.py")], cwd=root)
html = (root / "gathers" / "index.html").read_text(encoding="utf-8")
paths = set(re.findall(r'src="(\.\./assets/img/[^"]+)"', html))
missing = [p for p in sorted(paths) if not (root / p[3:]).is_file()]
print("imgs", len(paths), "missing", len(missing), "grids", html.count("img-grid"))
for m in missing:
    print("MISS", m)
