#!/usr/bin/env python3
"""Convert YouTube HTML articles to Hugo posts."""
import os
import re
from pathlib import Path
from datetime import datetime

REPO_ROOT = Path(r"C:\Users\11132\.qclaw\workspace-yw3plsutb1jupnif")
HTML_DIR = REPO_ROOT / "youtube_videos"
POSTS_DIR = REPO_ROOT / "content" / "posts"


def extract_title(html: str) -> str:
    m = re.search(r'<title>([^<]+)</title>', html)
    if m:
        return m.group(1).strip()
    m = re.search(r'<h1[^>]*>([^<]+)</h1>', html)
    if m:
        return m.group(1).strip()
    return "Untitled"


def extract_subtitle(html: str) -> str:
    m = re.search(r'class="subtitle"[^>]*>([^<]+)</div>', html)
    if m:
        return m.group(1).strip()
    return ""


def extract_css(html: str) -> str:
    m = re.search(r'<style[^>]*>(.*?)</style>', html, re.DOTALL)
    if m:
        return m.group(1).strip()
    return ""


def extract_body(html: str) -> str:
    # Try content div first
    m = re.search(r'<div class="content"[^>]*>(.*?)<div class="footer"', html, re.DOTALL)
    if m:
        body = m.group(1).strip()
    else:
        m = re.search(r'<div class="content">(.*?)<div class="footer">', html, re.DOTALL)
        if m:
            body = m.group(1).strip()
        else:
            # Fallback
            start = html.find('<div class="content">')
            end = html.rfind('<div class="footer">')
            if start >= 0 and end > start:
                body = html[start + len('<div class="content">'):end].strip()
            else:
                return ""

    # De-indent all lines (avoid Hugo goldmark treating as code blocks)
    lines = body.split('\n')
    clean = []
    for line in lines:
        t = line.strip()
        clean.append(t if t else '')
    return '\n'.join(clean).strip()


def escape_desc(s: str) -> str:
    return s.replace('\\', '\\\\').replace('"', '\\"')


def convert_all(video_id=None):
    if video_id:
        html_file = HTML_DIR / f"{video_id}_wechat_article.html"
        html_files = [html_file] if html_file.exists() else []
    else:
        html_files = list(HTML_DIR.glob("*_wechat_article.html"))
    print(f"HTML source: {HTML_DIR}")
    print(f"Output dir: {POSTS_DIR}")
    print(f"Found {len(html_files)} HTML files")
    print()

    processed = 0
    skipped = 0

    for hf in html_files:
        vid = hf.stem.replace('_wechat_article', '')
        if not re.match(r'^[a-zA-Z0-9_-]+$', vid):
            print(f"[SKIP] Bad filename: {hf.name}")
            skipped += 1
            continue

        html = hf.read_text(encoding='utf-8')
        title = extract_title(html)
        subtitle = extract_subtitle(html)
        css = extract_css(html)
        body = extract_body(html)

        if not body:
            print(f"[WARN] No body: {hf.name}")
            skipped += 1
            continue

        mtime = hf.stat().st_mtime
        dt = datetime.fromtimestamp(mtime)
        date_str = dt.strftime('%Y-%m-%dT%H:%M:%S+08:00')

        desc = escape_desc(subtitle) if subtitle else title

        post_dir = POSTS_DIR / vid
        post_dir.mkdir(parents=True, exist_ok=True)
        post_file = post_dir / "index.md"

        content = f"""---
title: "{title}"
date: {date_str}
draft: false
description: "{desc}"
---

{{< inline_style >}}
{css}
{{< /inline_style >}}

{body}
"""
        post_file.write_text(content, encoding='utf-8')
        print(f"[OK] {vid} -> content/posts/{vid}/index.md ({len(content)} bytes)")
        processed += 1

    print()
    print(f"Done: {processed} converted, {skipped} skipped")


if __name__ == "__main__":
    import sys
    vid = sys.argv[1] if len(sys.argv) > 1 else None
    convert_all(video_id=vid)
