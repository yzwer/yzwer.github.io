# -*- coding: utf-8 -*-
"""Publish article to WeChat Official Account draft box - Fixed version"""
import json
import urllib.request
import urllib.parse
import ssl
import os
import re

APP_ID = 'wxabc1784dbf87c3de'
APP_SECRET = '10d4335f33efcb36d3f27551870595d5'
ssl_ctx = ssl.create_default_context()

def get_access_token():
    url = f'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APP_ID}&secret={APP_SECRET}'
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, context=ssl_ctx, timeout=15) as resp:
        data = json.loads(resp.read().decode())
    if 'access_token' not in data:
        print(f'ERROR getting token: {data}')
        return None
    print(f'[OK] Access token obtained, expires in {data.get("expires_in")}s')
    return data['access_token']

def find_cover_image():
    """Find a suitable cover image"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    frames_dir = os.path.join(base_dir, 'frames')
    
    # Try frames directory first
    if os.path.isdir(frames_dir):
        for f in sorted(os.listdir(frames_dir)):
            if f.lower().endswith(('.jpg', '.jpeg', '.png')):
                return os.path.join(frames_dir, f)
    
    # Try current directory
    for f in os.listdir(base_dir):
        if f.lower().endswith(('.jpg', '.jpeg', '.png')) and 'cover' in f.lower():
            return os.path.join(base_dir, f)
    
    return None

def upload_thumb_image(token, image_path):
    """Upload thumbnail using urllib (multipart/form-data)"""
    import uuid
    boundary = uuid.uuid4().hex
    url = f'https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={token}&type=image'
    
    with open(image_path, 'rb') as f:
        file_data = f.read()
    
    filename = os.path.basename(image_path)
    
    body = bytearray()
    body.extend(f'--{boundary}\r\n'.encode('utf-8'))
    body.extend(f'Content-Disposition: form-data; name="media"; filename="{filename}"\r\n'.encode('utf-8'))
    body.extend(b'Content-Type: image/jpeg\r\n\r\n')
    body.extend(file_data)
    body.extend(f'\r\n--{boundary}--\r\n'.encode('utf-8'))
    
    req = urllib.request.Request(url, data=bytes(body), headers={
        'Content-Type': f'multipart/form-data; boundary={boundary}'
    })
    
    try:
        with urllib.request.urlopen(req, context=ssl_ctx, timeout=60) as resp:
            result = json.loads(resp.read().decode())
        print(f'[OK] Image uploaded, media_id: {result.get("media_id","")}')
        return result.get('media_id', '')
    except urllib.error.HTTPError as e:
        err_body = e.read().decode('utf-8', errors='replace')
        print(f'ERROR uploading image: {err_body}')
        return ''
    except Exception as e:
        print(f'ERROR uploading image: {e}')
        return ''

def create_draft(token, title, content, thumb_media_id=''):
    """Create draft article"""
    url = f'https://api.weixin.qq.com/cgi-bin/draft/add?access_token={token}'
    
    article = {
        "title": title,
        "author": "代码文学家",
        "digest": "死亡率60%、唯一人传人的病毒——汉坦病毒南极游轮事件完整还原",
        "content": content,
        "content_source_url": "",
        "thumb_media_id": thumb_media_id,
        "need_open_comment": 1,
        "only_fans_can_comment": 0
    }
    
    payload = json.dumps({"articles": [article]}, ensure_ascii=False).encode('utf-8')
    
    req = urllib.request.Request(url, data=payload, headers={
        'Content-Type': 'application/json; charset=utf-8'
    })
    
    try:
        with urllib.request.urlopen(req, context=ssl_ctx, timeout=30) as resp:
            result = json.loads(resp.read().decode())
        print(f'[OK] Draft created! Response: {json.dumps(result, ensure_ascii=False)}')
        return result
    except urllib.error.HTTPError as e:
        err_body = e.read().decode('utf-8', errors='replace')
        print(f'ERROR creating draft: {err_body}')
        return None
    except Exception as e:
        print(f'ERROR creating draft: {e}')
        return None

def read_html_content(html_path):
    """Read the HTML article and prepare for WeChat API"""
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Extract title
    title_match = re.search(r'<div class="ct-title">(.*?)</div>', html, re.DOTALL)
    title = re.sub(r'<[^>]+>', '', title_match.group(1)).replace('\n', ' ').strip() if title_match else '汉坦病毒游轮事件深度解读'
    
    # Extract content div
    match = re.search(r'<div class="c">(.*?)</div>\s*</div>\s*</body>', html, re.DOTALL)
    if not match:
        match = re.search(r'<div class="c">(.*)', html, re.DOTALL)
    
    if not match:
        print('ERROR: Could not extract article body')
        return title, ''
    
    body = match.group(1)
    
    # Convert to WeChat-compatible format
    # Remove HTML comments
    body = re.sub(r'<!-- .*? -->', '', body, flags=re.DOTALL)
    
    # Convert div.lead to p with inline style
    body = re.sub(r'<div class="lead">(.*?)</div>', r'<p style="color:#555;border-left:4px solid #e74c3c;padding-left:16px;margin:24px 0;line-height:2">\1</p>', body, flags=re.DOTALL)
    
    # Convert div.st to section with border
    body = re.sub(
        r'<div class="st"><span class="sn">(\d+)</span><span class="stx">(.*?)</span></div>',
        r'<section style="display:flex;align-items:center;margin:36px 0 18px"><span style="display:inline-flex;align-items:center;justify-content:center;width:36px;height:36px;background:linear-gradient(135deg,#e74c3c,#c0392b);color:#fff;font-size:18px;font-weight:800;border-radius:50%;margin-right:12px;flex-shrink:0">\1</span><span style="font-size:20px;font-weight:700;color:#1a1a1a">\2</span></section>',
        body
    )
    
    # Convert div.ic to section with background
    body = re.sub(
        r'<div class="ic">(.*?)</div>',
        r'<section style="background:#f8f9fa;border-radius:12px;padding:20px 22px;margin:24px 0;border-left:4px solid #3498db">\1</section>',
        body,
        flags=re.DOTALL
    )
    
    # Convert div.wc to section with red background
    body = re.sub(
        r'<div class="wc">(.*?)</div>',
        r'<section style="background:#fff5f5;border-radius:12px;padding:20px 22px;margin:24px 0;border-left:4px solid #e74c3c">\1</section>',
        body,
        flags=re.DOTALL
    )
    
    # Convert div.sg to table (WeChat doesn't support grid)
    body = re.sub(r'<div class="sg">(.*?)</div>', r'<table style="width:100%;margin:20px 0"><tr>\1</tr></table>', body, flags=re.DOTALL)
    body = re.sub(r'<div class="sb (sp|sr)">(.*?)</div>', r'<td style="width:50%;padding:18px;border-radius:10px;vertical-align:top">\2</td>', body, flags=re.DOTALL)
    
    # Convert div.sc to section with dark background
    body = re.sub(
        r'<div class="sc">(.*?)</div>',
        r'<section style="background:linear-gradient(135deg,#1a3a5c,#0d4a6b);border-radius:14px;padding:28px 24px;margin:32px 0;color:#fff">\1</section>',
        body,
        flags=re.DOTALL
    )
    
    # Convert div.tl to div with left border
    body = re.sub(r'<div class="tl">(.*?)</div>', r'<div style="position:relative;padding-left:28px;margin:24px 0">\1</div>', body, flags=re.DOTALL)
    
    # Convert span.hl to span with highlight
    body = re.sub(r'<span class="hl">(.*?)</span>', r'<span style="background:linear-gradient(to top,rgba(255,200,0,.25) 40%,transparent 40%);padding:0 2px;font-weight:600">\1</span>', body)
    
    # Convert span.hr to span with red highlight
    body = re.sub(r'<span class="hr">(.*?)</span>', r'<span style="background:linear-gradient(to top,rgba(231,76,60,.2) 40%,transparent 40%);padding:0 2px;font-weight:600;color:#c0392b">\1</span>', body)
    
    # Convert table.ct2
    # Keep tables as-is, WeChat supports them
    
    # Convert div.dv to hr
    body = re.sub(r'<div class="dv"></div>', r'<hr style="border:none;height:1px;background:linear-gradient(to right,transparent,#ddd,transparent);margin:32px 0">', body)
    
    # Convert div.ft to center text
    body = re.sub(r'<div class="ft">(.*?)</div>', r'<div style="text-align:center;padding:24px;color:#999;font-size:13px">\1</div>', body, flags=re.DOTALL)
    
    # Remove remaining class-based divs, keep content
    # (any unhandled divs will just be rendered as plain divs by WeChat)
    
    return title, body

# ===== MAIN =====
print('='*50)
print('WeChat Official Account Draft Publisher (Fixed)')
print('='*50)

html_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sojKNj_uXYU_wechat_article.html')

# Step 1: Get token
print('\n[1/3] Getting access token...')
token = get_access_token()
if not token:
    exit(1)

# Step 2: Read and convert article
print('\n[2/3] Reading article content...')
title, content = read_html_content(html_path)
print(f'Title: {title}')
print(f'Content length: {len(content)} chars')

if not content:
    print('ERROR: No content extracted!')
    exit(1)

# Step 3: Try uploading image (optional)
thumb_id = ''
img_path = find_cover_image()
if img_path:
    print(f'\n[Optional] Uploading cover image: {img_path}')
    thumb_id = upload_thumb_image(token, img_path)

# Step 4: Create draft
print('\n[3/3] Creating draft...')
result = create_draft(token, title, content, thumb_id)

if result and 'media_id' in result:
    print(f'\n SUCCESS! Draft created.')
    print(f'Media ID: {result["media_id"]}')
    print(f'You can now find it in 微信公众号后台 → 草稿箱')
elif result and 'errcode' in result:
    print(f'\n API Error: {result["errmsg"]} (code: {result["errcode"]})')
    # If image was the problem, retry without it
    if thumb_id and result.get('errcode') == 40007:
        print('Retrying without thumbnail...')
        result = create_draft(token, title, content)
        if result and 'media_id' in result:
            print(f'\n SUCCESS (no thumbnail)! Media ID: {result["media_id"]}')
else:
    print('\nCheck error messages above.')
