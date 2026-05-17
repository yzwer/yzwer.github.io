#!/usr/bin/env python3
"""Convert wechat_article.html files into Hugo posts (content/posts/<id>/index.md)."""
import os
import re
import sys
import json

SOURCE_DIR = r"C:\Users\11132\.qclaw\workspace-yw3plsutb1jupnif\youtube_videos"
REPO_DIR = r"D:\code_projects\vibecoding\yzwer.github.io"
POSTS_DIR = os.path.join(REPO_DIR, "content", "posts")
STATE_FILE = os.path.join(REPO_DIR, ".claude", "uploaded_files.txt")


def extract_title(html):
    m = re.search(r'<title>([^<]+)</title>', html)
    return m.group(1).strip() if m else "无标题"


def extract_body(html):
    m = re.search(r'<body[^>]*>(.*?)</body>', html, re.DOTALL)
    return m.group(1).strip() if m else html


def extract_tags(html):
    """Extract tags from footer divs like <span>tag</span> in .ft container."""
    tags = []
    # Find the last .ft div which contains tag spans
    m = re.search(r'<div class="ft">(.*?)</div>', html, re.DOTALL)
    if m:
        tags = re.findall(r'<span>([^<]+)</span>', m.group(1))
    return tags


def fix_section_headings(body):
    """Convert <div class="st"> section titles to markdown ## headings so Hugo TOC detects them."""
    body = re.sub(
        r'<div class="st">\s*<span class="sn">([^<]*)</span>\s*<span class="stx">([^<]*)</span>\s*</div>',
        r'\n\n## <span class="sn">\1</span>\2\n\n',
        body
    )
    return body


def extract_description(html, title):
    """Try to get a description from the .ct-sub or .lead div."""
    m = re.search(r'<div class="ct-sub">([^<]+)</div>', html, re.DOTALL)
    if m:
        desc = m.group(1).strip()
        desc = re.sub(r'<br\s*/?>', ' ', desc)
        return desc
    # Fall back to first paragraph
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

    os.makedirs(post_dir, exist_ok=True)

    # Convert <div class="st"> to <h2> for TOC support
    body = fix_section_headings(body)

    # Build tags YAML with safe quoting
    tags_yaml = ""
    if tags:
        tags_list = "\n".join(f'  - {json.dumps(t, ensure_ascii=False)}' for t in tags)
        tags_yaml = f"tags:\n{tags_list}\n"

    # Use JSON dumps for safe YAML quoting (handles quotes, newlines, etc.)
    safe_title = json.dumps(title, ensure_ascii=False)
    safe_desc = json.dumps(description, ensure_ascii=False)

    md_content = f"""---
title: {safe_title}
date: 2026-05-17
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
    # Check if a specific file was given, otherwise scan all
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
