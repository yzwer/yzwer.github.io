# -*- coding: utf-8 -*-
"""每日YouTube视频处理脚本"""
import json, os, sys, subprocess, urllib.request, time, re
sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"C:\Users\11132\.qclaw\workspace-yw3plsutb1jupnif\youtube_videos"
os.chdir(BASE_DIR)

APPID = "wxabc1784dbf87c3de"
SECRET = "10d4335f33efcb36d3f27551870595d5"

def get_latest_videos():
    """获取频道最新视频列表"""
    for attempt in range(3):
        try:
            result = subprocess.run(
                ["yt-dlp", "--flat-playlist", "-J", "https://www.youtube.com/@sunriches/videos"],
                capture_output=True, text=True, timeout=120, encoding='utf-8'
            )
            if result.returncode == 0 and result.stdout.strip():
                data = json.loads(result.stdout)
                entries = data.get('entries', [])
                return [(e['id'], e.get('title', '')) for e in entries if 'id' in e]
            # Try parsing stderr might have the JSON
            if result.stdout.strip():
                try:
                    data = json.loads(result.stdout)
                    entries = data.get('entries', [])
                    return [(e['id'], e.get('title', '')) for e in entries if 'id' in e]
                except:
                    pass
        except Exception as e:
            print(f"  重试 {attempt+1}/3: {e}")
            time.sleep(5 * (attempt + 1))
    return None

def get_last_video_id():
    """读取上次处理的视频ID"""
    try:
        with open('last_video.txt', 'r') as f:
            return f.read().strip()
    except:
        return None

def download_video(vid):
    """下载视频"""
    for attempt in range(3):
        try:
            result = subprocess.run(
                ["yt-dlp", "-f", "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
                 "--merge-output-format", "mp4", "-o", f"{vid}.%(ext)s",
                 f"https://www.youtube.com/watch?v={vid}"],
                capture_output=True, text=True, timeout=600, encoding='utf-8'
            )
            if os.path.exists(f"{vid}.mp4"):
                print(f"  ✅ 视频下载完成")
                return True
            print(f"  重试 {attempt+1}/3...")
            time.sleep(5)
        except Exception as e:
            print(f"  下载异常 {attempt+1}/3: {e}")
            time.sleep(5)
    return False

def extract_audio(vid):
    """提取音频"""
    if os.path.exists(f"{vid}.wav"):
        print(f"  ✅ 音频已存在")
        return True
    for attempt in range(3):
        try:
            result = subprocess.run(
                ["ffmpeg", "-y", "-i", f"{vid}.mp4",
                 "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1",
                 f"{vid}.wav"],
                capture_output=True, text=True, timeout=300
            )
            if os.path.exists(f"{vid}.wav"):
                print(f"  ✅ 音频提取完成")
                return True
            print(f"  重试 {attempt+1}/3...")
            time.sleep(5)
        except Exception as e:
            print(f"  音频提取异常 {attempt+1}/3: {e}")
            time.sleep(5)
    return False

def whisper_transcribe(vid):
    """Whisper转录"""
    if os.path.exists(f"{vid}.json"):
        print(f"  ✅ 转录已存在")
        return True
    for attempt in range(3):
        try:
            result = subprocess.run(
                ["whisper", f"{vid}.wav", "--model", "base", "--language", "zh",
                 "--output_format", "json", "--output_dir", "."],
                capture_output=True, text=True, timeout=600, encoding='utf-8'
            )
            if os.path.exists(f"{vid}.json"):
                print(f"  ✅ 转录完成")
                return True
            print(f"  重试 {attempt+1}/3...")
            time.sleep(5)
        except Exception as e:
            print(f"  转录异常 {attempt+1}/3: {e}")
            time.sleep(5)
    return False

def upload_cover(token, vid):
    """上传封面"""
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
        if 'media_id' in d:
            return d['media_id']
        else:
            print(f"  ⚠️ 封面上传失败: {d}")
            return None
    except Exception as e:
        print(f"  ⚠️ 封面上传异常: {e}")
        return None

def get_token():
    """获取access_token"""
    for attempt in range(3):
        try:
            url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APPID}&secret={SECRET}"
            with urllib.request.urlopen(url, timeout=10) as r:
                d = json.loads(r.read().decode())
            if 'access_token' in d:
                return d
            if d.get('errcode') == 40164:
                # IP白名单错误
                return d
            print(f"  Token重试 {attempt+1}/3: {d}")
            time.sleep(5)
        except Exception as e:
            print(f"  Token异常 {attempt+1}/3: {e}")
            time.sleep(5)
    return None

def publish_draft(token, vid, title, digest, html_content, thumb_media_id=None):
    """发布草稿"""
    article = {
        "title": title,
        "author": "OpenClaw",
        "digest": digest,
        "content": html_content,
        "content_source_url": f"https://www.youtube.com/watch?v={vid}",
        "need_open_comment": 1,
        "only_fans_can_comment": 0
    }
    if thumb_media_id:
        article["thumb_media_id"] = thumb_media_id
    for attempt in range(3):
        try:
            payload = json.dumps({"articles": [article]}, ensure_ascii=False).encode('utf-8')
            url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={token}"
            req = urllib.request.Request(url, data=payload, method='POST')
            req.add_header('Content-Type', 'application/json; charset=utf-8')
            with urllib.request.urlopen(req, timeout=30) as r:
                d = json.loads(r.read().decode())
            return d
        except Exception as e:
            print(f"  发布重试 {attempt+1}/3: {e}")
            time.sleep(5)
    return None

# === 主流程 ===
print("=== 每日YouTube视频检查 ===\n")

# Step 1: 获取最新视频列表
print("[1/5] 获取频道最新视频...")
videos = get_latest_videos()
if not videos:
    print("❌ 无法获取视频列表")
    sys.exit(1)

last_id = get_last_video_id()
print(f"  上次处理: {last_id}")
print(f"  最新视频: {videos[0][0]} - {videos[0][1]}")

# 判断新视频
new_videos = []
for vid, title in videos:
    if vid == last_id:
        break
    new_videos.append((vid, title))

if not new_videos:
    print("\n📭 今日检查 @sunriches 频道，暂无新视频发布。")
    sys.exit(0)

print(f"  发现 {len(new_videos)} 个新视频")
for vid, title in new_videos:
    print(f"    - {vid}: {title}")

# 只处理最新的1个视频（避免超时）
vid, orig_title = new_videos[0]
print(f"\n处理最新视频: {vid} - {orig_title}")

# Step 2: 下载
print(f"\n[2/5] 下载视频 {vid}...")
if not download_video(vid):
    print("❌ 视频下载失败")
    sys.exit(1)

# Step 3: 转录
print(f"\n[3/5] Whisper转录...")
if not extract_audio(vid):
    print("❌ 音频提取失败")
    sys.exit(1)
if not whisper_transcribe(vid):
    print("❌ 转录失败")
    sys.exit(1)

# Step 4: 读取转录内容，生成文章
print(f"\n[4/5] 生成公众号文章...")
with open(f"{vid}.json", 'r', encoding='utf-8') as f:
    data = json.load(f)
segments = data.get('segments', [])
full_text = ' '.join([s['text'] for s in segments])
print(f"  转录片段: {len(segments)}, 总字数: {len(full_text)}")
print(f"  ⚠️ 注意：文章需人工生成高质量HTML，此处仅输出转录摘要")
print(f"  转录前200字: {full_text[:200]}")

# 输出完整转录供后续人工生成文章
with open(f"{vid}_transcript.txt", 'w', encoding='utf-8') as f:
    for s in segments:
        start = int(s['start'])
        m, sec = divmod(start, 60)
        f.write(f"[{m:02d}:{sec:02d}] {s['text']}\n")
print(f"  转录已保存: {vid}_transcript.txt")

# Step 5: 发布
print(f"\n[5/5] 发布到公众号...")
token_result = get_token()
if not token_result:
    print("❌ 获取token失败")
    sys.exit(1)
if 'errcode' in token_result and token_result.get('errcode') == 40164:
    # 获取当前IP
    try:
        with urllib.request.urlopen("https://httpbin.org/ip", timeout=10) as r:
            ip_info = json.loads(r.read().decode())
        current_ip = ip_info.get('origin', 'unknown')
    except:
        current_ip = 'unknown'
    print(f"❌ IP白名单错误！请将 {current_ip} 添加到微信公众号后台白名单")
    sys.exit(1)

token = token_result['access_token']
print(f"  ✅ token获取成功")

# 上传封面
thumb = upload_cover(token, vid)
if thumb:
    print(f"  ✅ 封面上传成功: {thumb}")
else:
    print(f"  ⚠️ 无封面，继续发布")

# 生成基础HTML（后续需用高质量模板替换）
html = f'''<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8"><title>待编辑</title></head>
<body><p>待生成高质量文章内容</p></body></html>'''

# 使用自创标题（从内容提炼，不用原标题）
title = "新视频文章（待编辑）"
digest = full_text[:120]

result = publish_draft(token, vid, title, digest, html, thumb)
if result and 'media_id' in result:
    print(f"  ✅ 草稿发布成功: {result['media_id']}")
    with open('last_video.txt', 'w') as f:
        f.write(vid)
    print(f"  ✅ last_video.txt 已更新为 {vid}")
else:
    print(f"  ❌ 发布失败: {result}")

print("\n=== 完成 ===")
