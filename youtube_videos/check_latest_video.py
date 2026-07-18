import subprocess, json, sys

# 运行 yt-dlp 获取视频列表
cmd = ['yt-dlp', '--flat-playlist', '-J', 'https://www.youtube.com/@sunriches/videos']
result = subprocess.run(cmd, capture_output=True, text=True)

if result.returncode != 0:
    print(f'ERROR: {result.stderr}')
    sys.exit(1)

# 解析 JSON
try:
    data = json.loads(result.stdout)
    entries = data['entries']
    
    # 获取最新视频
    latest = entries[0]
    video_id = latest['id']
    title = latest.get('title', 'N/A')
    
    print(f'Latest video ID: {video_id}')
    print(f'Title: {title}')
    print(f'Duration: {latest.get("duration", "N/A")}')
    
except Exception as e:
    print(f'Parse error: {e}')
    sys.exit(1)
