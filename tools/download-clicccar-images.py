# -*- coding: utf-8 -*-
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"


def download_from_html(html_path: Path, subdir: str, pattern: str, base_url: str):
    html = html_path.read_text(encoding="utf-8")
    names = sorted(set(re.findall(pattern, html)))
    out = ROOT / "assets" / "img" / "clicccar" / subdir
    out.mkdir(parents=True, exist_ok=True)
    for name in names:
        p = out / name
        if p.exists():
            continue
        url = f"{base_url}/{name}"
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                p.write_bytes(r.read())
            print("ok", name)
        except Exception as e:
            print("fail", name, e)
    print(subdir, "files", len(list(out.glob("*.jpg"))))


if __name__ == "__main__":
    download_from_html(
        ROOT / "tmp" / "clicccar_1317716.html",
        "1317716",
        r"uploads/2023/10/03/(st12[^\"'?]+\-200x\d+\.jpg)",
        "https://clicccar.com/uploads/2023/10/03",
    )
    p3854 = ROOT / "tmp" / "clicccar_1313854.html"
    if p3854.exists():
        download_from_html(
            p3854,
            "1313854",
            r"uploads/2023/09/22/(st10[^\"'?]+\.(?:200x\d+|133x200)\.jpg)",
            "https://clicccar.com/uploads/2023/09/22",
        )
