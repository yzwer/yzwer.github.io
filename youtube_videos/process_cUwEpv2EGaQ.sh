#!/bin/bash
# 完整处理视频 cUwEpv2EGaQ 并发布到公众号

VID="cUwEpv2EGaQ"
BASE_DIR="$HOME/.qclaw/workspace-yw3plsutb1jupnif/youtube_videos"
cd "$BASE_DIR"

echo "=== 处理视频 $VID ==="

# 1. 下载视频和字幕（如果不存在）
if [ ! -f "${VID}.mp4" ]; then
    echo "[1/5] 下载视频..."
    yt-dlp -f "bestvideo[height<=1080]+bestaudio/best[height<=1080]" \
        --merge-output-format mp4 \
        -o "${VID}.%(ext)s" \
        "https://www.youtube.com/watch?v=${VID}"
else
    echo "[1/5] 视频已存在，跳过下载"
fi

# 2. 提取音频（如果不存在）
if [ ! -f "${VID}.wav" ]; then
    echo "[2/5] 提取音频..."
    ffmpeg -i "${VID}.mp4" -vn -acodec pcm_s16le -ar 16000 -ac 1 "${VID}.wav" -y
else
    echo "[2/5] 音频已存在，跳过提取"
fi

# 3. Whisper 转录（如果不存在）
if [ ! -f "${VID}.json" ]; then
    echo "[3/5] Whisper 转录..."
    whisper "${VID}.wav" --model medium --language zh --output_format json --output_dir .
    mv "${VID}.json" "${VID}.json" 2>/dev/null || true
else
    echo "[3/5] 转录已存在，跳过"
fi

# 4. 生成公众号文章 HTML
echo "[4/5] 生成公众号文章..."
python3 << 'PYTHON_SCRIPT'
import json, sys, os

vid = "cUwEpv2EGaQ"
base_dir = os.environ.get('BASE_DIR', '.')

# 读取转录结果
with open(f'{vid}.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

segments = data.get('segments', [])
full_text = data.get('text', '')

# 生成HTML
html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{data.get('title', '视频内容')}</title>
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
    <h1>🎬 {data.get('title', '视频内容')}</h1>
    <div class="summary">
        <p><strong>视频简介：</strong>{data.get('description', '')[:200]}...</p>
        <p><strong>时长：</strong>{data.get('duration', 'N/A')} 秒</p>
        <p><strong>转录时长：</strong>{len(segments)} 个片段</p>
    </div>
    <div class="transcript">
        <h2>📝 完整转录</h2>
'''

for seg in segments:
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

with open(f'{vid}_wechat_article.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"✅ HTML 文章已生成：{vid}_wechat_article.html")
print(f"   文件大小：{os.path.getsize(f'{vid}_wechat_article.html')} 字节")
PYTHON_SCRIPT

# 5. 发布到公众号草稿箱
echo "[5/5] 发布到公众号..."
python3 << 'PYTHON_SCRIPT'
import json, os, sys, urllib.request, urllib.parse, time

VID = "cUwEpv2EGaQ"
APPID = "wxabc1784dbf87c3de"
SECRET = "10d4335f33efcb36d3f27551870595d5"

# 读取 access token
token_url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APPID}&secret={SECRET}"
try:
    with urllib.request.urlopen(token_url, timeout=10) as response:
        token_data = json.loads(response.read().decode('utf-8'))
        ACCESS_TOKEN = token_data.get('access_token')
        if not ACCESS_TOKEN:
            print(f"❌ 获取 access_token 失败：{token_data}")
            sys.exit(1)
except Exception as e:
    print(f"❌ 网络错误：{e}")
    sys.exit(1)

print(f"✅ 获取 access_token 成功")

# 读取 HTML 文章
html_path = f"{VID}_wechat_article.html"
with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

# 准备草稿素材
draft_data = {
    "articles": [{
        "title": "视频转录文章",
        "author": "OpenClaw",
        "digest": "自动生成的视频转录文章",
        "content": html_content,
        "content_source_url": f"https://www.youtube.com/watch?v={VID}",
        "thumb_media_id": "",  # 需要先上传封面图
        "need_open_comment": 1,
        "only_fans_can_comment": 0
    }]
}

# 发布草稿
draft_url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={ACCESS_TOKEN}"
data = json.dumps(draft_data).encode('utf-8')
req = urllib.request.Request(draft_url, data=data, method='POST')
req.add_header('Content-Type', 'application/json')

try:
    with urllib.request.urlopen(req, timeout=30) as response:
        result = json.loads(response.read().decode('utf-8'))
        if 'media_id' in result:
            print(f"✅ 草稿发布成功！media_id: {result['media_id']}")
            # 更新 last_video.txt
            with open('last_video.txt', 'w') as f:
                f.write(VID)
            print(f"✅ 已更新 last_video.txt: {VID}")
        else:
            print(f"❌ 发布失败：{result}")
except Exception as e:
    print(f"❌ 发布错误：{e}")

PYTHON_SCRIPT

echo ""
echo "=== 处理完成 ==="
echo "视频 ID: $VID"
echo "HTML 文章: ${VID}_wechat_article.html"
echo "请检查公众号草稿箱"
