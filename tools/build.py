"""Build the static site from the canvas exports in source/.

Each source/*.dc.html is a Design-canvas artboard: page styles live in
<helmet>, the page itself inside <x-dc>, and images are referenced as
/_blob/<id>. This turns each one into a plain HTML page that loads the
same styles and serves images from images/<id>.jpg.

    python3 tools/build.py
"""
import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

PAGES = [
    ("Main.dc.html", "index.html",
     "How a state-aware cart revamp made delivery, savings and checkout readiness clear for Supertails shoppers."),
    ("Process.dc.html", "process.html",
     "Proto-personas, competitive learnings, a validation plan and draft explorations behind the Supertails cart revamp."),
]
LINKS = {"Main.dc.html": "index.html", "Process.dc.html": "process.html"}


def build(src_name, out_name, description):
    src = (ROOT / "source" / src_name).read_text()
    helmet = re.search(r"<helmet>(.*?)</helmet>", src, re.S).group(1).strip()
    body = re.search(r"<x-dc>(.*?)</x-dc>", src, re.S).group(1)
    body = re.sub(r"<helmet>.*?</helmet>", "", body, flags=re.S).strip()
    title = re.search(r"<title>(.*?)</title>", src).group(1)

    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · Supertails</title>
<meta name="description" content="{html.escape(description)}">
<meta property="og:title" content="{title} · Supertails">
<meta property="og:description" content="{html.escape(description)}">
<meta property="og:type" content="article">
{helmet}
</head>
<body>
{body}
</body>
</html>
"""
    page = re.sub(r"/_blob/([0-9a-f]{32})", r"images/\1.jpg", page)
    for dc, out in LINKS.items():
        page = page.replace(f'href="{dc}"', f'href="{out}"')

    missing = sorted({m for m in re.findall(r"images/([0-9a-f]{32})\.jpg", page)
                      if not (ROOT / "images" / f"{m}.jpg").exists()})
    if missing:
        raise SystemExit(f"{src_name}: missing images {missing}")
    (ROOT / out_name).write_text(page)
    print(f"{src_name} -> {out_name}")


for src_name, out_name, description in PAGES:
    build(src_name, out_name, description)
