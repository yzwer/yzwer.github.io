# -*- coding: utf-8 -*-
"""发布 cUwEpv2EGaQ 到公众号草稿箱（修复版）"""
import json, os, sys, urllib.request, urllib.parse, subprocess, base64
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
    """从视频截取封面并上传，返回 media_id；失败返回 None"""
    cover_jpg = f"cover_{vid}.jpg"
    # 截取第30秒帧
    if not os.path.exists(cover_jpg):
        subprocess.run(
            ["ffmpeg", "-y", "-i", f"{vid}.mp4", "-ss", "00:00:30",
             "-vframes", "1", "-q:v", "2", cover_jpg],
            capture_output=True, timeout=30
        )
    if not os.path.exists(cover_jpg):
        print("  ⚠️  无法生成封面图，跳过")
        return None

    # 构造 multipart/form-data
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

    # 读取视频标题
    with open(f"{vid}.json", 'r', encoding='utf-8') as f:
        data = json.load(f)
    title = data.get('title', '视频内容')[:64]

    article = {
        "title": title,
        "author": "OpenClaw",
        "digest": title[:120],
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

print("=== 发布 cUwEpv2EGaQ ===\n")

# Step 1: 获取 token
print("[1/3] 获取 access_token...")
token = get_token()
print(f"  ✅ token 获取成功")

# Step 2: 上传封面（可选）
print("\n[2/3] 处理封面图...")
thumb_media_id = upload_cover(token, VID)

# Step 3: 发布草稿
print("\n[3/3] 发布草稿...")
result = publish(token, VID, thumb_media_id)

if 'media_id' in result:
    print(f"\n✅ 发布成功！")
    print(f"   media_id = {result['media_id']}")
    with open('last_video.txt', 'w') as f:
        f.write(VID)
    print(f"   last_video.txt 已更新为 {VID}")
else:
    print(f"\n❌ 发布失败: {result}")

# 清理临时封面
try:
    os.remove(f"cover_{VID}.jpg")
except:
    pass

print("\n=== 完成 ===")
