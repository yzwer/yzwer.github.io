# -*- coding: utf-8 -*-
"""Publish articles to WeChat draft box - aOuFC_wWJo8 and 4IIJY9Y5L54"""
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

# Step 1: Get access token
print('[1/4] Getting access token...')
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
        sys.exit(2)  # Special exit code for IP whitelist issue
    print(f'FATAL: Token error: {token_result}')
    sys.exit(1)

access_token = token_result['access_token']
print(f'  Token OK (len={len(access_token)})')

# Articles to publish
articles = [
    {
        'vid': 'aOuFC_wWJo8',
        'title': '几个留学生犯案，轰动了整个欧洲：中国版"恩浩房"事件全记录',
        'digest': '一群中国留学生在德国合伙迷奸同胞，核心群组8人协作，下游群组4500人，运营长达4年。',
        'tag': '深度调查',
    },
    {
        'vid': '4IIJY9Y5L54',
        'title': '这场顶级饭局，细节全在座位里',
        'digest': '从国宴合影看社交密码与权力秩序——雷军找马斯克合影引发全网争议的背后逻辑。',
        'tag': '深度解读',
    },
]

results = []
for idx, art in enumerate(articles):
    vid = art['vid']
    print(f'\n[{idx+2}/4] Processing {vid}: {art["title"][:30]}...')

    # Extract cover image
    cover_jpg = os.path.join(base, f'cover_{vid}.jpg')
    if not os.path.exists(cover_jpg):
        mp4_file = os.path.join(base, f'{vid}.mp4')
        subprocess.run(['ffmpeg','-y','-i',mp4_file,'-ss','00:00:30','-vframes','1',cover_jpg],
                       capture_output=True, text=True, timeout=30)

    # Upload cover
    media_id = None
    if os.path.exists(cover_jpg):
        upload_url = f'https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={access_token}&type=image'
        upload_result = api_upload(upload_url, cover_jpg)
        if upload_result and 'media_id' in upload_result:
            media_id = upload_result['media_id']
            print(f'  Cover uploaded: media_id={media_id}')
        else:
            print(f'  Cover upload failed: {upload_result}')

    # Read article HTML
    html_file = os.path.join(base, f'{vid}_wechat_article.html')
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Create draft
    draft_url = f'https://api.weixin.qq.com/cgi-bin/draft/add?access_token={access_token}'
    draft_data = {
        "articles": [{
            "title": art['title'],
            "author": art['tag'],
            "digest": art['digest'],
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
        print(f'  Draft OK: {draft_result["media_id"]}')
        results.append((vid, 'SUCCESS', draft_result['media_id']))
    else:
        print(f'  Draft failed: {draft_result}')
        results.append((vid, 'FAILED', str(draft_result)))

    # Cleanup cover
    try:
        if os.path.exists(cover_jpg): os.remove(cover_jpg)
    except:
        pass

# Update last_video.txt to the newest video
newest = '4IIJY9Y5L54'
with open(os.path.join(base, 'last_video.txt'), 'w', encoding='utf-8') as f:
    f.write(newest)
print(f'\nlast_video.txt updated to: {newest}')

# Summary
print('\n=== RESULTS ===')
for vid, status, detail in results:
    print(f'  {vid}: {status} ({detail})')
print('DONE')
