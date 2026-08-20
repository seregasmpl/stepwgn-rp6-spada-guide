# -*- coding: utf-8 -*-
from pathlib import Path
import subprocess
import sys
import re

root = Path(__file__).resolve().parents[1]
for script in ("annotate-gathers-ru.py", "inject-gathers-photos.py", "build-gathers-site.py"):
    print("RUN", script)
    subprocess.check_call([sys.executable, str(root / "tools" / script)], cwd=root)

html = (root / "gathers" / "index.html").read_text(encoding="utf-8")
paths = set(re.findall(r'src="(\.\./assets/img/[^"]+)"', html))
missing = [p for p in sorted(paths) if not (root / p[3:]).is_file()]
main = (root / "index.html").read_text(encoding="utf-8")
print("gathers imgs", len(paths), "missing", len(missing), "grids", html.count("img-grid"))
print("main gathers-ru", main.count("gathers-ru/"), "jp1320797", main.count("clicccar/1320797/"))
for m in missing[:10]:
    print("MISS", m)
