#!/usr/bin/env python3
"""
YouTube 视频自动处理管道 v2.1
- 自动检测 Clash 代理端口 (优先 6789, 7890, 1080)
- 下载视频 + 提取音频 + Whisper 转录
- 转录成功即更新 last_video.txt
"""
import os
import sys
import json
import time
import socket
import subprocess
from pathlib import Path
from datetime import datetime

# ========== 配置 ==========
WORK_DIR = Path("C:/Users/11132/.qclaw/workspace-yw3plsutb1jupnif/youtube_videos")
CHANNEL_URL = "https://www.youtube.com/@sunriches/videos"

# 自动检测可用代理端口
def detect_proxy_port():
    """检测 Clash 可用端口，返回 proxy 参数或 None (直连)"""
    ports_to_try = [6789, 7890, 7891, 1080, 8080]
    for port in ports_to_try:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(2)
                result = s.connect_ex(('127.0.0.1', port))
                if result == 0:
                    print(f"[Proxy] Detected Clash on port {port}")
                    return f"socks5://127.0.0.1:{port}"
        except Exception:
            pass
    print("[Proxy] WARNING: No local proxy detected, trying direct (TUN mode?)")
    return None  # 直连（依赖 TUN 模式）

PROXY = detect_proxy_port()
PROXY_ARG = f'--proxy={PROXY} ' if PROXY else '--proxy= '

# ========== 日志 ==========
def log(msg):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    line = f"[{timestamp}] {msg}"
    log_file = WORK_DIR / "pipeline.log"
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(line + '\n')
    try:
        print(line, flush=True)
    except UnicodeEncodeError:
        safe_line = line.encode('gbk', errors='replace').decode('gbk')
        print(safe_line, flush=True)

def run_cmd(cmd, retries=3, timeout=600):
    for attempt in range(1, retries + 1):
        log(f"[{attempt}/{retries}] {cmd[:80]}...")
        try:
            result = subprocess.run(
                cmd, shell=True, timeout=timeout,
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
            if result.returncode == 0:
                log("[OK]")
                return True, ""
            else:
                log(f"[ERROR] rc={result.returncode}")
        except subprocess.TimeoutExpired:
            log(f"[ERROR] timeout({timeout}s)")
        except Exception as e:
            log(f"[ERROR] {e}")
        if attempt < retries:
            time.sleep(5 * attempt)
    return False, ""

def get_latest_videos(count=3):
    log(f"Fetching latest {count} videos...")
    temp_file = WORK_DIR / "temp_videos.json"
    proxy_arg = PROXY_ARG if 'PROXY_ARG' in dir() else '--proxy= '
    cmd = f'yt-dlp {PROXY_ARG}"--flat-playlist" -J "{CHANNEL_URL}" > "{temp_file}" 2>NUL'
    # 简化：直接用 Python 调用 yt-dlp
    import yt_dlp
    try:
        ydl_opts = {'quiet': True, 'proxy': PROXY, 'retries': 2, 'socket_timeout': 30}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(CHANNEL_URL, download=False)
            videos = [{'id': e['id'], 'title': e.get('title', 'N/A')} for e in info['entries'][:count]]
            return videos
    except Exception as e:
        raise Exception(f"yt-dlp failed: {e}")

def get_last_video_id():
    f = WORK_DIR / "last_video.txt"
    return f.read_text(encoding='utf-8').strip() if f.exists() else None

def save_last_video_id(vid):
    f = WORK_DIR / "last_video.txt"
    with open(f, 'w', encoding='utf-8') as fh:
        fh.write(vid)
    log(f"Updated last_video.txt: {vid}")

def process_video(video_id, title):
    log("=" * 60)
    log(f"Processing: {video_id} - {title}")
    log("=" * 60)

    try:
        # [1/4] Download
        mp4 = WORK_DIR / f"{video_id}.mp4"
        if not mp4.exists():
            log("[1/4] Downloading...")
            cmd = f'yt-dlp {PROXY_ARG}-f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best" -o "{WORK_DIR}/{video_id}.%(ext)s" "https://www.youtube.com/watch?v={video_id}"'
            ok, _ = run_cmd(cmd, retries=3, timeout=600)
            if not ok:
                raise Exception("Download failed")
        else:
            log("[1/4] Video exists, skip")

        # [2/4] Extract audio
        wav = WORK_DIR / f"{video_id}.wav"
        if not wav.exists():
            log("[2/4] Extracting audio...")
            cmd = f'ffmpeg -i "{WORK_DIR}/{video_id}.mp4" -vn -acodec pcm_s16le -ar 16000 -ac 1 "{wav}" -y'
            ok, _ = run_cmd(cmd, retries=3, timeout=300)
            if not ok:
                raise Exception("Audio extraction failed")
        else:
            log("[2/4] Audio exists, skip")

        # [3/4] Whisper
        jsn = WORK_DIR / f"{video_id}.json"
        if not jsn.exists():
            log("[3/4] Whisper transcribing...")
            cmd = f'whisper "{wav}" --model base --language zh --output_format json --output_dir "{WORK_DIR}"'
            ok, _ = run_cmd(cmd, retries=2, timeout=1200)
            if not ok:
                raise Exception("Whisper failed")
        else:
            log("[3/4] Transcript exists, skip")

        # Transcription done -> update last_video.txt immediately
        save_last_video_id(video_id)
        log(f"[OK] {video_id} transcribed. last_video.txt updated.")

        # [4/4] Upload (best effort, don't block on IP whitelist)
        html = WORK_DIR / f"{video_id}_wechat_article.html"
        if not html.exists():
            log("[4/4] No article HTML yet, skip upload. AI will generate later.")
        else:
            log("[4/4] Uploading draft...")
            upload_script = WORK_DIR / "upload_draft.py"
            if upload_script.exists():
                cmd = f'python "{upload_script}" "{video_id}"'
                ok, _ = run_cmd(cmd, retries=2, timeout=300)
                if ok:
                    log("[OK] Draft uploaded!")
                else:
                    log("[WARN] Upload failed (likely IP whitelist)")
            else:
                log("[WARN] upload_draft.py not found")

        log("=" * 60)
        return True

    except Exception as e:
        log(f"[ERROR] {video_id} failed: {e}")
        return False

def main():
    log("=" * 60)
    log("YouTube Pipeline v2.1 started")
    log(f"Proxy: {PROXY or 'DIRECT (TUN mode)'}")
    log("=" * 60)
    os.chdir(WORK_DIR)

    try:
        videos = get_latest_videos(count=3)
        last_id = get_last_video_id()
        log(f"Last processed: {last_id}")

        to_process = []
        for v in videos:
            if v['id'] != last_id:
                to_process.append(v)
            else:
                break

        if not to_process:
            log("No new videos. Done.")
            return

        log(f"Found {len(to_process)} new video(s)")
        ok_count = 0
        for v in reversed(to_process):
            if process_video(v['id'], v['title']):
                ok_count += 1

        log(f"Done! {ok_count}/{len(to_process)} succeeded")

    except Exception as e:
        log(f"[ERROR] {e}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        log(f"[FATAL] {e}")
        sys.exit(1)
