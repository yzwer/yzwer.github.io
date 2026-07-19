#!/usr/bin/env python3
"""
YouTube 视频自动处理管道 v2.3
- 自动确保 Clash 代理可用（检测端口，不通则重启 Clash）
- 支持 cookies 文件绕过 YouTube bot 检测
- 下载视频 + 提取音频 + Whisper 转录
- 转录成功即更新 last_video.txt
- 文章生成由 AI sub-agent 另行处理
"""
import os
import sys
import json
import time
import subprocess
from pathlib import Path
from datetime import datetime

# ========== 配置 ==========
WORK_DIR = Path("C:/Users/11132/.qclaw/workspace-yw3plsutb1jupnif/youtube_videos")
CHANNEL_URL = "https://www.youtube.com/@sunriches/videos"
COOKIES_FILE = WORK_DIR / "youtube_cookies.txt"  # Netscape format cookies

# ========== 确保 Clash 代理可用，获取代理参数 ==========
import subprocess as _sp

PROXY_ARG = ""   # 例如 "--proxy=socks5://127.0.0.1:6789 "
COOKIES_ARG = ""  # 例如 "--cookies youtube_cookies.txt"
# yt-dlp 2025+ 需要 JS 运行时解密 YouTube 签名，否则只能拿到缩略图
# 默认只启用 deno，本机未装 deno 故显式启用 node
YTDLP_EXTRA = "--js-runtimes node --remote-components ejs:github --no-check-certificates "
_ensure = WORK_DIR / "ensure_clash.py"
if _ensure.exists():
    _r = _sp.run([sys.executable, str(_ensure)], capture_output=True, text=True, timeout=120)
    if _r.returncode != 0:
        # ensure_clash.py 向 stderr 打日志，stdout 为空
        _err = _r.stderr.strip() or _r.stdout.strip()
        print(f"[WARN] Clash proxy NOT available: {_err[:100]}", file=sys.stderr)
    else:
        # ensure_clash.py 成功时 stdout 只有端口号，例如 "6789"
        _port = _r.stdout.strip()
        if _port.isdigit():
            PROXY_ARG = f"--proxy=socks5://127.0.0.1:{_port} "
            print(f"[Pipeline] Using proxy: {PROXY_ARG.strip()}")
        else:
            print(f"[WARN] Cannot parse proxy port from: {repr(_port)}", file=sys.stderr)
else:
    print("[WARN] ensure_clash.py not found, running without proxy", file=sys.stderr)

# Cookies
if COOKIES_FILE.exists():
    COOKIES_ARG = f'--cookies "{COOKIES_FILE}" '
    print(f"[Pipeline] Using cookies: {COOKIES_FILE}")
else:
    print("[Pipeline] No cookies file found. YouTube may require authentication.")

print(f"[Pipeline] PROXY_ARG='{PROXY_ARG.strip()}'")

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
    stderr_accumulated = ""
    for attempt in range(1, retries + 1):
        log(f"[{attempt}/{retries}] {cmd[:80]}...")
        try:
            result = subprocess.run(
                cmd, shell=True, timeout=timeout,
                capture_output=True, text=True
            )
            if result.returncode == 0:
                log("[OK]")
                return True, result.stdout
            else:
                log(f"[ERROR] rc={result.returncode}")
                stderr_accumulated += result.stderr + "\n"
        except subprocess.TimeoutExpired:
            log(f"[ERROR] timeout({timeout}s)")
        except Exception as e:
            log(f"[ERROR] {e}")
        if attempt < retries:
            time.sleep(5 * attempt)
    return False, stderr_accumulated

def get_latest_videos(count=3):
    log(f"Fetching latest {count} videos...")
    temp_file = WORK_DIR / "temp_videos.json"
    cmd = f'yt-dlp {PROXY_ARG}{COOKIES_ARG}{YTDLP_EXTRA}--flat-playlist -J "{CHANNEL_URL}" > "{temp_file}" 2>NUL'
    success, _ = run_cmd(cmd, retries=3)
    if not success:
        raise Exception("Failed to fetch video list")
    try:
        data = json.loads(temp_file.read_text(encoding='utf-8-sig'))
        videos = [{'id': e['id'], 'title': e.get('title', 'N/A')} for e in data['entries'][:count]]
        return videos
    except Exception as e:
        raise Exception(f"Parse error: {e}")
    finally:
        if temp_file.exists():
            temp_file.unlink()

def get_last_video_id():
    f = WORK_DIR / "last_video.txt"
    return f.read_text(encoding='utf-8').strip() if f.exists() else None

def save_last_video_id(vid):
    f = WORK_DIR / "last_video.txt"
    with open(f, 'w', encoding='utf-8') as fh:
        fh.write(vid)
    log(f"Updated last_video.txt: {vid}")

def is_members_only(video_id):
    """Check if a video is members-only"""
    cmd = f'yt-dlp {PROXY_ARG}{COOKIES_ARG}{YTDLP_EXTRA}--print "%(is_members_only)s" "https://www.youtube.com/watch?v={video_id}"'
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        return 'True' in result.stdout
    except Exception:
        return False


def process_video(video_id, title):
    log("=" * 60)
    log(f"Processing: {video_id} - {title}")
    log("=" * 60)

    try:
        # [1/4] Download
        mp4 = WORK_DIR / f"{video_id}.mp4"
        if not mp4.exists():
            log("[1/4] Downloading...")
            cmd = f'yt-dlp {PROXY_ARG}{COOKIES_ARG}{YTDLP_EXTRA}-f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best" -o "{WORK_DIR}/{video_id}.%(ext)s" "https://www.youtube.com/watch?v={video_id}"'
            ok, stderr = run_cmd(cmd, retries=3, timeout=600)
            if not ok:
                # Check if it's members-only
                if stderr and ('members-only' in stderr or 'Join this channel' in stderr):
                    log(f"[SKIP] {video_id} is members-only, skipping")
                    save_last_video_id(video_id)
                    return True  # Skip, don't block
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
            # 使用 faster-whisper（原版 whisper 在 Python 3.14 上会卡住）
            script = WORK_DIR / "whisper_transcribe.py"
            cmd = f'python -u "{script}" "{wav}" "{WORK_DIR}/{video_id}.json" base zh'
            ok, _ = run_cmd(cmd, retries=2, timeout=1800)
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

def _convert_html_to_hugo(video_id, html_file, repo_root):
    """Convert HTML article to Hugo post format."""
    import re
    try:
        import subprocess as _sp3
        script = repo_root / "convert_youtube_to_hugo.py"
        if not script.exists():
            log(f"[Hugo] convert_youtube_to_hugo.py not found, skipping Hugo conversion")
            return
        result = _sp3.run(
            [sys.executable, str(script), video_id],
            capture_output=True, text=True, timeout=30, cwd=str(repo_root)
        )
        if result.returncode == 0 and "[OK]" in result.stdout:
            log(f"[Hugo] Converted {video_id} to Hugo post")
        else:
            log(f"[Hugo] Conversion output: {result.stdout[:100]} {result.stderr[:100]}")
    except Exception as _e:
        log(f"[Hugo] Conversion error: {_e}")


def main():
    log("=" * 60)
    log("YouTube Pipeline v2.3 started")
    log(f"Proxy: {PROXY_ARG.strip() or 'NONE (direct)'}")
    log("=" * 60)
    os.chdir(WORK_DIR)

    _repo_root = Path("C:/Users/11132/.qclaw/workspace-yw3plsutb1jupnif")

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

        # ===== Hugo: Convert any new HTML articles to Hugo posts =====
        for v in reversed(to_process):
            vid = v['id']
            html_file = WORK_DIR / f"{vid}_wechat_article.html"
            if html_file.exists():
                _convert_html_to_hugo(vid, html_file, _repo_root)
            else:
                log(f"[Hugo] No HTML article yet for {vid}, skipping Hugo conversion")

        # ===== Git Push (youtube_videos + content/posts) =====
        try:
            import subprocess as _sp2
            # Check for uncommitted changes in both youtube_videos and content/posts
            _st = _sp2.run(["git", "status", "--porcelain"], capture_output=True, text=True,
                           cwd=str(_repo_root), timeout=10)
            if _st.stdout.strip():
                log("[Git] Uncommitted changes, committing and pushing...")
                _sp2.run(["git", "add", "-A", "youtube_videos/", "content/posts/"],
                         cwd=str(_repo_root), timeout=10)
                _ci = _sp2.run(["git", "commit", "-m",
                               f"youtube: pipeline run {datetime.now().strftime('%Y-%m-%d %H:%M')} + Hugo posts"],
                               capture_output=True, text=True, cwd=str(_repo_root), timeout=10)
                if _ci.returncode == 0:
                    log(f"[Git] Committed: {_ci.stdout[:200]}")
                    _push = _sp2.run(
                        ["git", "push", "origin", "master"],
                        capture_output=True, text=True,
                        cwd=str(_repo_root),
                        env={**os.environ, "GIT_HTTP_PROXY": "http://127.0.0.1:6789"},
                        timeout=60
                    )
                    if _push.returncode == 0:
                        log(f"[Git] Push succeeded")
                    else:
                        log(f"[Git] Push failed: {_push.stderr[:200]}")
                else:
                    log(f"[Git] Commit failed: {_ci.stderr[:200]}")
            else:
                log("[Git] No new changes to push")
        except Exception as _ge:
            log(f"[Git] Push error: {_ge}")

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
