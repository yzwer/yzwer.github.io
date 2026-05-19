#!/usr/bin/env python3
"""Convert wechat_article.html files into Hugo posts (content/posts/<id>/index.md)."""
import os
import re
import sys
import json
from datetime import datetime, timezone

SOURCE_DIR = r"C:\Users\11132\.qclaw\workspace-yw3plsutb1jupnif\youtube_videos"
REPO_DIR = r"D:\code_projects\vibecoding\yzwer.github.io"
POSTS_DIR = os.path.join(REPO_DIR, "content", "posts")
STATE_FILE = os.path.join(REPO_DIR, ".claude", "uploaded_files.txt")

# Default gradient cover CSS — always injected for a consistent look
DEFAULT_COVER_CSS = """
.aw{max-width:960px;margin:0 auto;background:#fff}
.cover{height:380px;background:linear-gradient(135deg,#0a1628,#1a3a5c,#0d4a6b);display:flex;align-items:center;justify-content:center;position:relative;overflow:hidden}
.cover::before{content:'';position:absolute;top:-50%;left:-50%;width:200%;height:200%;background:radial-gradient(circle at 30% 70%,rgba(255,80,80,.15),transparent 50%),radial-gradient(circle at 70% 30%,rgba(0,200,255,.1),transparent 50%);animation:pulse 6s ease-in-out infinite}
@keyframes pulse{0%,100%{opacity:.6}50%{opacity:1}}
.ct{position:relative;z-index:2;text-align:center;padding:40px}
.ct-tag{display:inline-block;background:rgba(255,80,80,.9);color:#fff;font-size:13px;padding:4px 16px;border-radius:20px;margin-bottom:20px;letter-spacing:2px}
.ct-title{font-size:30px;font-weight:800;color:#fff;line-height:1.4;margin-bottom:16px;text-shadow:0 2px 20px rgba(0,0,0,.5)}
.ct-sub{font-size:15px;color:rgba(255,255,255,.7);line-height:1.6}
.c{max-width:960px;margin:0 auto;background:#fff;padding:30px 24px 40px}
"""

# Common article content styles (WeChat-style cards, lists, etc.)
CONTENT_COMMON_CSS = """
.c p{margin-bottom:18px;font-size:16px;text-align:justify}
.lead{font-size:17px;color:#555;border-left:4px solid #e74c3c;padding-left:16px;margin:24px 0;line-height:2}
.ic{background:#f8f9fa;border-radius:12px;padding:20px 22px;margin:24px 0;border-left:4px solid #3498db}
.ic h4{font-size:16px;color:#2c3e50;margin-bottom:12px}
.ic li{font-size:15px;color:#555;padding:6px 0 6px 20px;position:relative;line-height:1.7;list-style:none}
.ic li::before{content:'\\2022';color:#3498db;font-weight:bold;position:absolute;left:0}
.wc{background:#fff5f5;border-radius:12px;padding:20px 22px;margin:24px 0;border-left:4px solid #e74c3c}
.wc h4{font-size:16px;color:#c0392b;margin-bottom:12px}
.sg{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:20px 0}
.sb{border-radius:10px;padding:18px;text-align:center}
.sp{background:linear-gradient(135deg,#fff5f5,#ffe8e8);border:1px solid #ffcdd2}
.sr{background:linear-gradient(135deg,#fff8e1,#ffecb3);border:1px solid #ffe082}
.sc{background:linear-gradient(135deg,#1a3a5c,#0d4a6b);border-radius:14px;padding:28px 24px;margin:32px 0;color:#fff}
.sc h4{font-size:18px;margin-bottom:16px}
.sc li{font-size:15px;padding:6px 0 6px 18px;position:relative;line-height:1.8;opacity:.9;list-style:none}
.sc li::before{content:'\\2713';position:absolute;left:0;color:#4fc3f7}
.dv{height:1px;background:linear-gradient(to right,transparent,#ddd,transparent);margin:32px 0}
.ft{text-align:center;padding:24px;color:#999;font-size:13px}
.ft span{display:inline-block;background:#f0f0f0;padding:4px 14px;border-radius:20px;margin:4px}
.sn{display:inline-flex;align-items:center;justify-content:center;width:36px;height:36px;background:linear-gradient(135deg,#e74c3c,#c0392b);color:#fff;font-size:18px;font-weight:800;border-radius:50%;margin-right:12px;flex-shrink:0}
.ct2{width:100%;border-collapse:separate;border-spacing:0;margin:20px 0;border-radius:10px;overflow:hidden;box-shadow:0 2px 12px rgba(0,0,0,.08)}
.ct2 th{background:linear-gradient(135deg,#2c3e50,#34495e);color:#fff;padding:14px 16px;font-size:14px;font-weight:600;text-align:center}
.ct2 td{padding:12px 16px;font-size:14px;text-align:center;border-bottom:1px solid #eee}
.ct2 tr:nth-child(even) td{background:#f8f9fa}
.tl2{font-weight:700;color:#2c3e50;text-align:left!important}
"""


def strip_existing_wrapper(body):
    """If body already has an .aw wrapper (Type A), strip cover + wrapper,
    keeping only the inner content from inside .c."""
    if not re.search(r'<div\s+class="aw">', body):
        return body  # Type B — no wrapper to strip
    # Extract content inside <div class="c">...</div> which is inside .aw
    m = re.search(r'<div\s+class="c">(.*)</div>\s*</div>\s*$', body, re.DOTALL)
    if m:
        return m.group(1).strip()
    return body


def strip_boilerplate(body):
    """Remove source attribution, boilerplate text, and empty dividers."""
    # Remove <p class="source"> or <p class="source-*">
    body = re.sub(r'<p\s+class="source[^"]*">[^<]*</p>\s*', '', body)
    # Remove <div class="source">...</div>
    body = re.sub(r'<div\s+class="source[^"]*">.*?</div>\s*', '', body, flags=re.DOTALL)
    # Remove trailing divider before source/footer
    body = re.sub(r'<div class="dv"></div>\s*$', '', body)
    return body


def build_article_body(body, title, tags, description):
    """Build cover + content sections.
    Headings are kept as ## markdown at the top level (outside <div> blocks)
    so Hugo's .TableOfContents can detect them."""
    # Strip existing cover/wrapper if present (Type A articles)
    body = strip_existing_wrapper(body)
    body = strip_boilerplate(body)

    # Cover section (standalone, not wrapping content)
    tag_html = f'<div class="ct-tag">{tags[0]}</div>\n' if tags else ""
    desc_html = f'<div class="ct-sub">{description}</div>\n' if description else ""
    cover = (
        f'<div class="aw">\n'
        f'<div class="cover">\n'
        f'<div class="ct">\n'
        f'{tag_html}<div class="ct-title">{title}</div>\n'
        f'{desc_html}</div>\n'
        f'</div>\n'
        f'</div>'
    )

    # Convert headings to ## markdown format
    # Type A: <div class="st"><span class="sn">N</span><span class="stx">Title</span></div>
    body = re.sub(
        r'<div class="st">\s*<span class="sn">([^<]*)</span>\s*<span class="stx">([^<]*)</span>\s*</div>',
        r'\n## <span class="sn">\1</span>\2\n',
        body
    )
    # Type B: <h2>Title</h2>
    body = re.sub(r'<h2>([^<]+)</h2>', r'\n## \1\n', body)

    # Remove optional <div class="container"> wrapper (Type B articles)
    body = re.sub(
        r'<div\s+class="container">\s*(.*)\s*</div>\s*$',
        r'\1',
        body,
        flags=re.DOTALL
    )
    body = body.strip()

    # Split at heading boundaries, wrap content blocks in <div class="c">
    parts = re.split(r'^(## .*)$', body, flags=re.MULTILINE)
    sections = [cover]
    more_inserted = False
    for part in parts:
        part = part.strip()
        if not part:
            continue
        if part.startswith('## '):
            sections.append(part)
        else:
            content = f'<div class="c">\n{part}\n</div>'
            if not more_inserted:
                content += '\n\n<!--more-->'
                more_inserted = True
            sections.append(content)

    return '\n\n'.join(sections)


def extract_title(html):
    m = re.search(r'<title>([^<]+)</title>', html)
    return m.group(1).strip() if m else "无标题"


def extract_body(html):
    m = re.search(r'<body[^>]*>(.*?)</body>', html, re.DOTALL)
    return m.group(1).strip() if m else html


def extract_tags(html):
    """Extract tags from footer divs like <span>tag</span> in .ft container."""
    tags = []
    m = re.search(r'<div class="ft">(.*?)</div>', html, re.DOTALL)
    if m:
        tags = re.findall(r'<span>([^<]+)</span>', m.group(1))
    return tags


def remove_duplicate_h1(body, title):
    """Remove <h1> that duplicates the cover title."""
    return re.sub(r'<h1>\s*' + re.escape(title) + r'\s*</h1>', '', body, flags=re.IGNORECASE)


def extract_style(html):
    """Extract <style> content from source HTML."""
    m = re.search(r'<style>(.*?)</style>', html, re.DOTALL)
    return m.group(1).strip() if m else ""


def clean_css(css):
    """Remove global/structural rules that would leak site-wide or override our cover layout."""
    css = re.sub(r'\*\s*\{[^}]*\}', '', css)
    css = re.sub(r'body\s*\{[^}]*\}', '', css)
    # Strip structural cover classes — these are owned by DEFAULT_COVER_CSS
    css = re.sub(r'\.(?:aw|cover|ct|c)\s*\{[^}]*\}', '', css)
    return css.strip()


def extract_description(html, title):
    """Try to get a description from the .ct-sub or .lead div."""
    m = re.search(r'<div class="ct-sub">([^<]+)</div>', html, re.DOTALL)
    if m:
        desc = m.group(1).strip()
        desc = re.sub(r'<br\s*/?>', ' ', desc)
        return desc
    m = re.search(r'<p>([^<]+)</p>', html)
    if m:
        return m.group(1).strip()[:100]
    return title


def convert_file(html_file):
    video_id = os.path.basename(html_file).replace('_wechat_article.html', '')
    post_dir = os.path.join(POSTS_DIR, video_id)

    with open(html_file, 'r', encoding='utf-8') as f:
        html = f.read()

    title = extract_title(html)
    description = extract_description(html, title)
    tags = extract_tags(html)
    body = extract_body(html)
    article_css = extract_style(html)

    os.makedirs(post_dir, exist_ok=True)

    # Remove duplicate <h1> (title already shown in cover)
    body = remove_duplicate_h1(body, title)

    # Build article body with cover + content sections
    body = build_article_body(body, title, tags, description)

    # Build article CSS: default cover + content styles + any source CSS
    css_parts = [DEFAULT_COVER_CSS, CONTENT_COMMON_CSS]
    if article_css:
        article_css = clean_css(article_css)
        if article_css.strip():
            css_parts.append(article_css)
    # Add default h2 style only if article doesn't define its own
    if not re.search(r'h2\s*\{', article_css):
        css_parts.append('h2{font-size:20px;font-weight:700;color:#2c3e50;margin:36px 0 18px;padding:0}')
    full_css = "\n".join(css_parts)

    # Prepend article CSS via Hugo shortcode (bypasses Goldmark style-tag stripping)
    body = f'{{{{< inline_style >}}}}{full_css}{{{{< /inline_style >}}}}\n{body}'

    # Build tags YAML with safe quoting
    tags_yaml = ""
    if tags:
        tags_list = "\n".join(f'  - {json.dumps(t, ensure_ascii=False)}' for t in tags)
        tags_yaml = f"tags:\n{tags_list}\n"

    # Use JSON dumps for safe YAML quoting
    safe_title = json.dumps(title, ensure_ascii=False)
    safe_desc = json.dumps(description, ensure_ascii=False)
    # Use source file's modification time for the date, converted to UTC date
    src_mtime = datetime.fromtimestamp(os.path.getmtime(html_file), timezone.utc)
    today = src_mtime.strftime('%Y-%m-%d')

    md_content = f"""---
title: {safe_title}
date: {today}
draft: false
description: {safe_desc}
{tags_yaml}---

{body}
"""

    out_path = os.path.join(post_dir, "index.md")
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(md_content)

    print(f"Created: {out_path}")
    return video_id


def main():
    if len(sys.argv) > 1:
        files = [sys.argv[1]]
    else:
        files = []
        for f in os.listdir(SOURCE_DIR):
            if f.endswith('_wechat_article.html'):
                files.append(os.path.join(SOURCE_DIR, f))

    if not files:
        print("No HTML files found.")
        return

    for f in sorted(files):
        convert_file(f)


if __name__ == '__main__':
    main()
