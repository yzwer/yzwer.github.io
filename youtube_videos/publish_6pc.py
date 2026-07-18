# -*- coding: utf-8 -*-
"""Publish 6PcC0ADq1zo to WeChat draft box"""
import json, os, sys, time, urllib.request, urllib.error, subprocess
sys.stdout.reconfigure(encoding='utf-8')

APPID = 'wxabc1784dbf87c3de'
SECRET = '10d4335f33efcb36d3f27551870595d5'
base = r'C:\Users\11132\.qclaw\workspace-yw3plsutb1jupnif\youtube_videos'

def api_get(url, retries=3):
    for i in range(retries):
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=15) as resp:
                return json.loads(resp.read().decode('utf-8'))
        except Exception as e:
            print(f'  API error (attempt {i+1}): {e}')
            if i < retries-1: time.sleep([5,15,30][i])
    return None

def api_post(url, data, retries=3):
    for i in range(retries):
        try:
            body = json.dumps(data, ensure_ascii=False).encode('utf-8')
            req = urllib.request.Request(url, data=body, method='POST')
            req.add_header('Content-Type', 'application/json; charset=utf-8')
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode('utf-8'))
        except Exception as e:
            print(f'  API error (attempt {i+1}): {e}')
            if i < retries-1: time.sleep([5,15,30][i])
    return None

def api_upload(url, filepath, retries=3):
    for i in range(retries):
        try:
            import mimetypes
            mime = mimetypes.guess_type(filepath)[0] or 'image/jpeg'
            filename = os.path.basename(filepath)
            with open(filepath, 'rb') as f:
                file_data = f.read()
            boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
            body = f'--{boundary}\r\nContent-Disposition: form-data; name="media"; filename="{filename}"\r\nContent-Type: {mime}\r\n\r\n'.encode('utf-8')
            body += file_data
            body += f'\r\n--{boundary}--\r\n'.encode('utf-8')
            req = urllib.request.Request(url, data=body, method='POST')
            req.add_header('Content-Type', f'multipart/form-data; boundary={boundary}')
            with urllib.request.urlopen(req, timeout=60) as resp:
                return json.loads(resp.read().decode('utf-8'))
        except Exception as e:
            print(f'  Upload error (attempt {i+1}): {e}')
            if i < retries-1: time.sleep([5,15,30][i])
    return None

print('[1/3] Getting access token...')
token_url = f'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APPID}&secret={SECRET}'
token_result = api_get(token_url)
if not token_result or 'access_token' not in token_result:
    errcode = token_result.get('errcode','') if token_result else ''
    if errcode == 40164:
        try:
            ip_req = urllib.request.Request('https://httpbin.org/ip')
            with urllib.request.urlopen(ip_req, timeout=10) as r:
                ip_info = json.loads(r.read().decode('utf-8'))
                outbound_ip = ip_info.get('origin','')
        except:
            outbound_ip = 'unknown'
        print(f'IP_WHITELIST_ERROR: {outbound_ip}')
        sys.exit(2)
    print(f'FATAL: Token error: {token_result}')
    sys.exit(1)

access_token = token_result['access_token']
print(f'  Token OK (len={len(access_token)})')

vid = '6PcC0ADq1zo'
print(f'\n[2/3] Processing {vid}...')

# Extract cover
cover_jpg = os.path.join(base, f'cover_{vid}.jpg')
if not os.path.exists(cover_jpg):
    mp4_file = os.path.join(base, f'{vid}.mp4')
    subprocess.run(['ffmpeg','-y','-i',mp4_file,'-ss','00:00:30','-vframes','1',cover_jpg],
                   capture_output=True, text=True, timeout=30)

media_id = None
if os.path.exists(cover_jpg):
    upload_url = f'https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={access_token}&type=image'
    upload_result = api_upload(upload_url, cover_jpg)
    if upload_result and 'media_id' in upload_result:
        media_id = upload_result['media_id']
        print(f'  Cover uploaded: {media_id}')
    else:
        print(f'  Cover upload failed: {upload_result}')

# Read article HTML
html_file = os.path.join(base, f'{vid}_wechat_article.html')
with open(html_file, 'r', encoding='utf-8') as f:
    html_content = f.read()
print(f'  HTML size: {len(html_content)} chars')

# Create draft
draft_url = f'https://api.weixin.qq.com/cgi-bin/draft/add?access_token={access_token}'
draft_data = {
    "articles": [{
        "title": "屡查屡犯、终酿惨剧：湖南浏阳烟花厂的24次查处与一场本可避免的爆炸",
        "author": "深度调查",
        "digest": "浏阳一家烟花厂历经24次查处仍违规生产，最终爆炸造成群死群伤——这是中国花炮之乡最惨痛的一课。",
        "content": html_content,
        "content_source_url": f"https://www.youtube.com/watch?v={vid}",
        "need_open_comment": 1,
        "only_fans_can_comment": 0
    }]
}
if media_id:
    draft_data["articles"][0]["thumb_media_id"] = media_id

draft_result = api_post(draft_url, draft_data)
if draft_result and 'media_id' in draft_result:
    print(f'\n✅ Draft OK! media_id={draft_result["media_id"]}')
else:
    print(f'\n❌ Draft failed: {draft_result}')

# Cleanup
try:
    if os.path.exists(cover_jpg): os.remove(cover_jpg)
except:
    pass

print('DONE')
