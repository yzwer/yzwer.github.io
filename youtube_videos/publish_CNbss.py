# -*- coding: utf-8 -*-
"""发布 CNbss-pyc18 到公众号草稿箱"""
import json, os, sys, urllib.request, subprocess
sys.stdout.reconfigure(encoding='utf-8')

VID = "CNbss-pyc18"
BASE_DIR = r"C:\Users\11132\.qclaw\workspace-yw3plsutb1jupnif\youtube_videos"
os.chdir(BASE_DIR)

APPID = "wxabc1784dbf87c3de"
SECRET = "10d4335f33efcb36d3f27551870595d5"

def get_token():
    for attempt in range(3):
        try:
            url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APPID}&secret={SECRET}"
            with urllib.request.urlopen(url, timeout=10) as r:
                d = json.loads(r.read().decode())
            if 'access_token' in d:
                return d
            if d.get('errcode') == 40164:
                try:
                    with urllib.request.urlopen("https://httpbin.org/ip", timeout=10) as r2:
                        ip_info = json.loads(r2.read().decode())
                    d['_current_ip'] = ip_info.get('origin', 'unknown')
                except:
                    d['_current_ip'] = 'unknown'
                return d
            import time; time.sleep(5)
        except Exception as e:
            print(f"  Token异常 {attempt+1}/3: {e}")
            import time; time.sleep(5)
    return None

def upload_cover(token, vid):
    cover_jpg = f"cover_{vid}.jpg"
    if not os.path.exists(cover_jpg):
        subprocess.run(
            ["ffmpeg", "-y", "-i", f"{vid}.mp4", "-ss", "00:00:30",
             "-vframes", "1", "-q:v", "2", cover_jpg],
            capture_output=True, timeout=30
        )
    if not os.path.exists(cover_jpg):
        return None
    boundary = b'----OpenClawBoundary7MA4YWxkTrZu0gW'
    with open(cover_jpg, 'rb') as f:
        img_data = f.read()
    body = b'--' + boundary + b'\r\n'
    body += b'Content-Disposition: form-data; name="media"; filename="cover.jpg"\r\n'
    body += b'Content-Type: image/jpeg\r\n\r\n'
    body += img_data
    body += b'\r\n--' + boundary + b'--\r\n'
    url = f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={token}&type=image"
    req = urllib.request.Request(url, data=body, method='POST')
    req.add_header('Content-Type', f'multipart/form-data; boundary={boundary.decode()}')
    req.add_header('Content-Length', str(len(body)))
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            d = json.loads(r.read().decode())
        return d.get('media_id')
    except Exception as e:
        print(f"  ⚠️ 封面上传异常: {e}")
        return None

def publish(token, vid, thumb_media_id=None):
    with open(f"{vid}_wechat_article.html", 'r', encoding='utf-8') as f:
        html = f.read()
    title = "贷款转负、社融腰斩：一份金融数据背后的经济真相"
    article = {
        "title": title,
        "author": "OpenClaw",
        "digest": "4月社融仅达预期一半，人民币贷款历史性负增长，全球市场暴跌——经济远比想象中承压",
        "content": html,
        "content_source_url": f"https://www.youtube.com/watch?v={vid}",
        "need_open_comment": 1,
        "only_fans_can_comment": 0
    }
    if thumb_media_id:
        article["thumb_media_id"] = thumb_media_id
    payload = json.dumps({"articles": [article]}, ensure_ascii=False).encode('utf-8')
    url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={token}"
    req = urllib.request.Request(url, data=payload, method='POST')
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())

print("=== 发布 CNbss-pyc18 ===\n")

print("[1/3] 获取 access_token...")
token_result = get_token()
if not token_result:
    print("❌ 获取token失败")
    sys.exit(1)
if token_result.get('errcode') == 40164:
    print(f"❌ IP白名单错误！当前出口IP: {token_result.get('_current_ip', 'unknown')}")
    print(f"   请将此IP添加到微信公众号后台白名单")
    sys.exit(1)

token = token_result['access_token']
print("  ✅ token获取成功")

print("\n[2/3] 上传封面...")
thumb = upload_cover(token, VID)
if thumb:
    print(f"  ✅ 封面上传成功: {thumb}")
else:
    print("  ⚠️ 无封面，继续")

print("\n[3/3] 发布草稿...")
result = publish(token, VID, thumb)
if result and 'media_id' in result:
    print(f"  ✅ 草稿发布成功！media_id: {result['media_id']}")
    with open('last_video.txt', 'w') as f:
        f.write(VID)
    print(f"  ✅ last_video.txt 已更新为 {VID}")
else:
    print(f"  ❌ 发布失败: {result}")

try:
    os.remove(f"cover_{VID}.jpg")
except:
    pass

print("\n=== 完成 ===")
