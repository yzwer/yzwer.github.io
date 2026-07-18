# -*- coding: utf-8 -*-
"""重新发布 cUwEpv2EGaQ（高质量文章）到公众号草稿箱"""
import json, os, sys, urllib.request, subprocess
sys.stdout.reconfigure(encoding='utf-8')

VID = "cUwEpv2EGaQ"
BASE_DIR = r"C:\Users\11132\.qclaw\workspace-yw3plsutb1jupnif\youtube_videos"
os.chdir(BASE_DIR)

APPID = "wxabc1784dbf87c3de"
SECRET = "10d4335f33efcb36d3f27551870595d5"

def get_token():
    url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APPID}&secret={SECRET}"
    with urllib.request.urlopen(url, timeout=10) as r:
        d = json.loads(r.read().decode())
    if 'errcode' in d:
        print(f"❌ Token error: {d}")
        sys.exit(1)
    return d['access_token']

def upload_cover(token, vid):
    cover_jpg = f"cover_{vid}.jpg"
    if not os.path.exists(cover_jpg):
        subprocess.run(
            ["ffmpeg", "-y", "-i", f"{vid}.mp4", "-ss", "00:00:30",
             "-vframes", "1", "-q:v", "2", cover_jpg],
            capture_output=True, timeout=30
        )
    if not os.path.exists(cover_jpg):
        print("  ⚠️  无法生成封面图，跳过")
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
        if 'media_id' in d:
            print(f"  ✅ 封面上传成功: {d['media_id']}")
            return d['media_id']
        else:
            print(f"  ⚠️  封面上传失败: {d}")
            return None
    except Exception as e:
        print(f"  ⚠️  封面上传异常: {e}")
        return None

def publish(token, vid, thumb_media_id):
    with open(f"{vid}_wechat_article.html", 'r', encoding='utf-8') as f:
        html = f.read()
    title = "从充电5分钟到网贷帮凶：一家千亿手机厂商的焦虑与迷失"
    article = {
        "title": title,
        "author": "OpenClaw",
        "digest": "母亲节文案翻车、网贷推送争议、自研芯片折戟、渠道体系崩盘——一家年营收千亿的手机厂商，如何在焦虑中一步步迷失方向",
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
        d = json.loads(r.read().decode())
    return d

print("=== 重新发布 cUwEpv2EGaQ（高质量版本） ===\n")

print("[1/3] 获取 access_token...")
token = get_token()
print("  ✅ token 获取成功")

print("\n[2/3] 上传封面图...")
thumb_media_id = upload_cover(token, VID)

print("\n[3/3] 发布草稿...")
result = publish(token, VID, thumb_media_id)

if 'media_id' in result:
    print(f"\n✅ 发布成功！")
    print(f"   media_id = {result['media_id']}")
    with open('last_video.txt', 'w') as f:
        f.write(VID)
    print(f"   last_video.txt 已更新")
else:
    print(f"\n❌ 发布失败: {result}")

try:
    os.remove(f"cover_{VID}.jpg")
except:
    pass

print("\n=== 完成 ===")
