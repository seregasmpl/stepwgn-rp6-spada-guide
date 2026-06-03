# -*- coding: utf-8 -*-
import re
from pathlib import Path

p = Path(__file__).resolve().parents[1] / "index.html"
html = p.read_text(encoding="utf-8")
# /> class="zoomable" -> class="zoomable" />
html = re.sub(r'/\s+(class="zoomable"[^>]*>)', r' \1', html)
html = re.sub(r'/\s+class="zoomable"', ' class="zoomable"', html)
p.write_text(html, encoding="utf-8")
print("fixed broken img closings")
