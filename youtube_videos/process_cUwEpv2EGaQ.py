# -*- coding: utf-8 -*-
"""完整处理视频 cUwEpv2EGaQ 并发布到公众号"""
import json, os, sys, time, urllib.request, urllib.parse, subprocess
sys.stdout.reconfigure(encoding='utf-8')

VID = "cUwEpv2EGaQ"
BASE_DIR = r"C:\Users\11132\.qclaw\workspace-yw3plsutb1jupnif\youtube_videos"
os.chdir(BASE_DIR)

print(f"=== 处理视频 {VID} ===\n")

# 1. 下载视频（如果不存在）
if not os.path.exists(f"{VID}.mp4"):
    print("[1/5] 下载视频...")
    result = subprocess.run([
        "yt-dlp", "-f", "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
        "--merge-output-format", "mp4",
        "-o", f"{VID}.%(ext)s",
        f"https://www.youtube.com/watch?v={VID}"
    ], capture_output=True, text=True)
    if result.returncode == 0:
        print("  ✅ 下载完成")
    else:
        print(f"  ❌ 下载失败：{result.stderr}")
        sys.exit(1)
else:
    print("[1/5] 视频已存在，跳过下载")

# 2. 提取音频（如果不存在）
if not os.path.exists(f"{VID}.wav"):
    print("[2/5] 提取音频...")
    result = subprocess.run([
        "ffmpeg", "-i", f"{VID}.mp4",
        "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1",
        f"{VID}.wav", "-y"
    ], capture_output=True, text=True, timeout=300)
    if result.returncode == 0:
        print("  ✅ 音频提取完成")
    else:
        print(f"  ❌ 音频提取失败：{result.stderr}")
        sys.exit(1)
else:
    print("[2/5] 音频已存在，跳过提取")

# 3. Whisper 转录（如果不存在）
if not os.path.exists(f"{VID}.json"):
    print("[3/5] Whisper 转录...")
    result = subprocess.run([
        "whisper", f"{VID}.wav",
        "--model", "medium", "--language", "zh",
        "--output_format", "json", "--output_dir", "."
    ], capture_output=True, text=True, timeout=600)
    if result.returncode == 0:
        # 重命名输出文件
        whisper_output = f"{VID}.json"
        if os.path.exists(whisper_output):
            print("  ✅ 转录完成")
        else:
            print(f"  ❌ 转录文件未找到")
            sys.exit(1)
    else:
        print(f"  ❌ 转录失败：{result.stderr}")
        sys.exit(1)
else:
    print("[3/5] 转录已存在，跳过")

# 4. 生成公众号文章 HTML
print("[4/5] 生成公众号文章...")

with open(f"{VID}.json", 'r', encoding='utf-8') as f:
    data = json.load(f)

segments = data.get('segments', [])
video_title = data.get('title', '视频内容')

html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{video_title}</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; line-height: 1.6; padding: 20px; max-width: 800px; margin: 0 auto; }}
        h1 {{ color: #333; border-bottom: 2px solid #1AAD19; padding-bottom: 10px; }}
        .transcript {{ background: #f8f8f8; padding: 15px; border-radius: 5px; margin: 20px 0; }}
        .segment {{ margin: 10px 0; }}
        .time {{ color: #1AAD19; font-size: 0.9em; }}
        .text {{ margin-left: 10px; }}
        .summary {{ background: #fff; border-left: 4px solid #1AAD19; padding: 15px; margin: 20px 0; }}
    </style>
</head>
<body>
    <h1>🎬 {video_title}</h1>
    <div class="summary">
        <p><strong>视频简介：</strong>{data.get('description', '')[:200]}...</p>
        <p><strong>时长：</strong>{data.get('duration', 'N/A')} 秒</p>
        <p><strong>转录片段数：</strong>{len(segments)} 个</p>
    </div>
    <div class="transcript">
        <h2>📝 完整转录</h2>
'''

for seg in segments[:50]:  # 只显示前50段避免HTML过大
    start = int(seg['start'])
    mins = start // 60
    secs = start % 60
    time_str = f"{mins:02d}:{secs:02d}"
    html += f'''        <div class="segment">
            <span class="time">[{time_str}]</span>
            <span class="text">{seg['text']}</span>
        </div>
'''

html += '''    </div>
    <hr>
    <p style="text-align: center; color: #999; font-size: 0.9em;">
        由 OpenClaw 自动生成 | <a href="https://www.youtube.com/watch?v=cUwEpv2EGaQ">观看原视频</a>
    </p>
</body>
</html>'''

with open(f"{VID}_wechat_article.html", 'w', encoding='utf-8') as f:
    f.write(html)

print(f"  ✅ HTML 文章已生成：{VID}_wechat_article.html")
print(f"     文件大小：{os.path.getsize(f'{VID}_wechat_article.html')} 字节")

# 5. 发布到公众号草稿箱
print("\n[5/5] 发布到公众号...")

APPID = "wxabc1784dbf87c3de"
SECRET = "10d4335f33efcb36d3f27551870595d5"

# 获取 access token
token_url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APPID}&secret={SECRET}"
try:
    with urllib.request.urlopen(token_url, timeout=10) as response:
        token_data = json.loads(response.read().decode('utf-8'))
        ACCESS_TOKEN = token_data.get('access_token')
        if not ACCESS_TOKEN:
            print(f"  ❌ 获取 access_token 失败：{token_data}")
            sys.exit(1)
except Exception as e:
    print(f"  ❌ 网络错误：{e}")
    sys.exit(1)

print(f"  ✅ 获取 access_token 成功")

# 读取 HTML 文章
html_path = f"{VID}_wechat_article.html"
with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

# 准备草稿数据
draft_data = {
    "articles": [{
        "title": video_title[:64],  # 微信限制标题长度
        "author": "OpenClaw",
        "digest": video_title[:120],  # 摘要
        "content": html_content,
        "content_source_url": f"https://www.youtube.com/watch?v={VID}",
        # "thumb_media_id": "",  # 不传封面字段，使用默认
        "need_open_comment": 1,
        "only_fans_can_comment": 0
    }]
}

# 发布草稿
draft_url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={ACCESS_TOKEN}"
data = json.dumps(draft_data, ensure_ascii=False).encode('utf-8')
req = urllib.request.Request(draft_url, data=data, method='POST')
req.add_header('Content-Type', 'application/json; charset=utf-8')

try:
    with urllib.request.urlopen(req, timeout=30) as response:
        result = json.loads(response.read().decode('utf-8'))
        if 'media_id' in result:
            print(f"  ✅ 草稿发布成功！media_id: {result['media_id']}")
            # 更新 last_video.txt
            with open('last_video.txt', 'w') as f:
                f.write(VID)
            print(f"  ✅ 已更新 last_video.txt: {VID}")
        else:
            print(f"  ❌ 发布失败：{result}")
            if result.get('errcode') == 40164:
                print("  ⚠️  IP 白名单错误，请将当前 IP 加入微信公众号后台白名单")
except Exception as e:
    print(f"  ❌ 发布错误：{e}")

print("\n=== 处理完成 ===")
print(f"视频 ID: {VID}")
print(f"HTML 文章: {VID}_wechat_article.html")
print("请检查公众号草稿箱")
