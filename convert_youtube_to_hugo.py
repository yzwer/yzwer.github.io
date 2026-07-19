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
    # Try content div first (new format)
    body = _try_extract_div(html, 'content', 'footer')
    if body:
        return body
    # Try container div (old format)
    body = _try_extract_div(html, 'container', None)
    if body:
        return body
    return ""


def _try_extract_div(html: str, div_class: str, end_marker: str) -> str:
    start_tag = f'<div class="{div_class}"'
    start = html.find(start_tag)
    if start < 0:
        start_tag = f'<div class="{div_class}">'
        start = html.find(start_tag)
    if start < 0:
        return ""
    # Find the opening div close >
    end_tag_pos = html.find('>', start)
    if end_tag_pos < 0:
        return ""
    content_start = end_tag_pos + 1
    if end_marker:
        end = html.rfind(f'<div class="{end_marker}"')
    else:
        end = html.rfind('</body>')
        if end < 0:
            end = len(html)
    if end <= content_start:
        return ""
    body = html[content_start:end].strip()
    # De-indent
    lines = body.split('\n')
    clean = [l.strip() if l.strip() else '' for l in lines]
    return '\n'.join(clean).strip()


def escape_yaml_str(s: str) -> str:
    """Escape a string for YAML double-quoted scalar.

    Handles: backslash, ASCII double-quote, newlines, tabs.
    Chinese/Japanese/Korean curly quotes (U+201C/U+201D) and em-dashes
    (U+2014) are NOT ASCII quotes and are valid in YAML double-quoted strings.
    """
    s = s.replace('\\', '\\\\')   # escape backslash first
    s = s.replace('"', '\\"')        # escape ASCII double-quote
    s = s.replace('\n', '\\n')       # escape newlines
    s = s.replace('\t', '\\t')       # escape tabs
    s = s.replace('\r', '\\r')       # escape carriage returns
    s = s.replace('\x00', '')          # remove NUL (invalid in YAML)
    return s


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

        desc = escape_yaml_str(subtitle) if subtitle else escape_yaml_str(title)
        safe_title = escape_yaml_str(title)

        post_dir = POSTS_DIR / vid
        post_dir.mkdir(parents=True, exist_ok=True)
        post_file = post_dir / "index.md"

        shortcode_open = "{{< inline_style >}}"
        shortcode_close = "{{< /inline_style >}}"
        content = (
            "---\n"
            f"title: \"{safe_title}\"\n"
            f"date: {date_str}\n"
            "draft: false\n"
            f'description: "{desc}"\n'
            "---\n\n"
            + shortcode_open + "\n"
            + css + "\n"
            + shortcode_close + "\n\n"
            + body
        )
        post_file.write_text(content, encoding='utf-8')
        print(f"[OK] {vid} -> content/posts/{vid}/index.md ({len(content)} bytes)")
        processed += 1

    print()
    print(f"Done: {processed} converted, {skipped} skipped")


if __name__ == "__main__":
    import sys
    vid = sys.argv[1] if len(sys.argv) > 1 else None
    convert_all(video_id=vid)
