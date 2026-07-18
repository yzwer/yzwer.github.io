#!/usr/bin/env python3
"""
YouTube 视频自动处理管道 - 完整版
执行流程：检查新视频(最近3个) → 下载 → 转录 → 生成文章 → 上传公众号 → 发布到 Hugo
"""
import os
import sys
import json
import time
import subprocess
import requests
from pathlib import Path

# ========== 配置 ==========
WORK_DIR = Path("C:/Users/11132/.qclaw/workspace-yw3plsutb1jupnif/youtube_videos")
APPID = "wxabc1784dbf87c3de"
APPSECRET = "10d4335f33efcb36d3f27551870595d5"
CHANNEL_URL = "https://www.youtube.com/@sunriches/videos"
MONITOR_SCRIPT = Path("D:/code_projects/vibecoding/yzwer.github.io/.claude/monitor_upload.sh")

# 禁用代理（微信公众号 API 不需要）
PROXIES = {'http': None, 'https': None}

# ========== 工具函数 ==========
def log(msg):
    """打印日志（兼容 Windows PowerShell GBK 编码）"""
    # 移除 emoji，避免 GBK 编码错误
    msg = msg.replace('✅', '[OK]').replace('❌', '[ERROR]').replace('⏳', '[...]')
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)

def run_cmd(cmd, retries=3):
    """执行命令，自动重试"""
    for i in range(retries):
        log(f"执行: {cmd[:80]}...")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=300)
        if result.returncode == 0:
            return result.stdout
        log(f"失败 (尝试 {i+1}/{retries}): {result.stderr[:200]}")
        time.sleep(5 * (i + 1))
    raise Exception(f"命令失败 after {retries} 次重试: {cmd[:100]}")

def get_access_token():
    """获取微信公众号 access_token"""
    url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APPID}&secret={APPSECRET}"
    resp = requests.get(url, proxies=PROXIES, timeout=10)
    data = resp.json()
    if 'errcode' in data and data['errcode'] != 0:
        raise Exception(f"获取 token 失败: {data}")
    return data['access_token']

def upload_thumb(video_id, token):
    """上传封面图到公众号"""
    # 如果封面不存在，用 ffmpeg 截取
    cover_path = WORK_DIR / f"{video_id}_cover.jpg"
    if not cover_path.exists():
        log(f"封面不存在，截取中...")
        cmd = f'ffmpeg -i "{WORK_DIR}/{video_id}.mp4" -ss 00:00:30 -vframes 1 "{cover_path}" -y'
        run_cmd(cmd)
    
    # 上传
    url = f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={token}&type=thumb"
    with open(cover_path, 'rb') as f:
        files = {'media': f}
        resp = requests.post(url, files=files, proxies=PROXIES, timeout=30)
    data = resp.json()
    if 'media_id' not in data:
        raise Exception(f"上传封面失败: {data}")
    return data['media_id']

def create_draft(video_id, thumb_media_id, token):
    """创建公众号草稿"""
    # 读取文章 HTML
    html_path = WORK_DIR / f"{video_id}_wechat_article.html"
    if not html_path.exists():
        raise Exception(f"文章 HTML 不存在: {html_path}")
    
    html_content = html_path.read_text(encoding='utf-8')
    
    # 提取标题（从 HTML 的 <title> 或第一个 <h1>）
    import re
    title_match = re.search(r'<title>(.*?)</title>', html_content)
    if not title_match:
        title_match = re.search(r'<h1[^>]*>(.*?)</h1>', html_content)
    title = title_match.group(1) if title_match else video_id
    
    # 构造草稿数据
    draft_data = {
        "articles": [{
            "title": title,
            "author": "阳光之下",
            "digest": title,
            "content": html_content,
            "content_source_url": "",
            "thumb_media_id": thumb_media_id,
            "need_open_comment": 0,
            "only_fans_can_comment": 0
        }]
    }
    
    # 调用 API
    url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={token}"
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    resp = requests.post(
        url,
        data=json.dumps(draft_data, ensure_ascii=False).encode('utf-8'),
        headers=headers,
        proxies=PROXIES,
        timeout=30
    )
    data = resp.json()
    if 'media_id' not in data:
        raise Exception(f"创建草稿失败: {data}")
    return data['media_id']

def process_video(video_id, title):
    """处理单个视频（完整流程）"""
    log(f"=" * 60)
    log(f"开始处理视频: {video_id}")
    log(f"标题: {title}")
    log(f"=" * 60)
    
    try:
        # [1/6] 下载视频
        log(f"[1/6] 下载视频...")
        if not (WORK_DIR / f"{video_id}.mp4").exists():
            cmd = f'yt-dlp -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best" -o "{WORK_DIR}/{video_id}.%(ext)s" "https://www.youtube.com/watch?v={video_id}"'
            run_cmd(cmd)
        else:
            log(f"[1/6] 视频已存在，跳过下载")
        
        # [2/6] 提取音频
        log(f"[2/6] 提取音频...")
        wav_path = WORK_DIR / f"{video_id}.wav"
        if not wav_path.exists():
            cmd = f'ffmpeg -i "{WORK_DIR}/{video_id}.mp4" -vn -acodec pcm_s16le -ar 16000 -ac 1 "{wav_path}" -y'
            run_cmd(cmd)
        else:
            log(f"[2/6] 音频已存在，跳过提取")
        
        # [3a/6] Whisper 转录
        log(f"[3a/6] Whisper 转录...")
        json_path = WORK_DIR / f"{video_id}.json"
        if not json_path.exists():
            # 使用 Python API 调用 Whisper（避免 CLI 问题）
            import whisper
            model = whisper.load_model("base")
            result = model.transcribe(str(wav_path), language="zh", fp16=False)
            
            # 保存为 JSON（兼容 yt-dlp 格式）
            segments = []
            for seg in result['segments']:
                segments.append({
                    'start': seg['start'],
                    'end': seg['end'],
                    'text': seg['text']
                })
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump({'segments': segments}, f, ensure_ascii=False, indent=2)
        else:
            log(f"[3a/6] 转录已存在，跳过")
        
        # [3b/6] 生成公众号文章
        log(f"[3b/6] 生成公众号文章...")
        html_path = WORK_DIR / f"{video_id}_wechat_article.html"
        if not html_path.exists():
            # 读取转录
            with open(json_path, 'r', encoding='utf-8') as f:
                transcript_data = json.load(f)
            
            # 这里需要调用文章生成逻辑（参考之前的代码）
            # 为简洁起见，这里调用外部 Python 脚本
            script_path = WORK_DIR / "generate_article.py"
            if script_path.exists():
                cmd = f'python "{script_path}" "{video_id}"'
                run_cmd(cmd)
            else:
                log(f"[3b/6] 警告: generate_article.py 不存在，跳过文章生成")
        else:
            log(f"[3b/6] 文章已存在，跳过生成")
        
        # [3c/6] 上传公众号草稿箱
        log(f"[3c/6] 上传公众号草稿箱...")
        token = get_access_token()
        log(f"[3c/6] Token 获取成功")
        
        thumb_media_id = upload_thumb(video_id, token)
        log(f"[3c/6] 封面上传成功: {thumb_media_id}")
        
        draft_media_id = create_draft(video_id, thumb_media_id, token)
        log(f"[3c/6] 草稿创建成功: {draft_media_id}")
        
        # [3d/6] 更新 last_video.txt
        log(f"[3d/6] 更新 last_video.txt...")
        with open(WORK_DIR / "last_video.txt", 'w', encoding='utf-8') as f:
            f.write(video_id)
        
        # [3e/6] 执行 monitor_upload.sh（发布到 Hugo）
        log(f"[3e/6] 发布到 Hugo 博客...")
        if MONITOR_SCRIPT.exists():
            cmd = f'bash "{MONITOR_SCRIPT}"'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=300)
            if result.returncode == 0:
                log(f"[3e/6] Hugo 发布成功")
            else:
                log(f"[3e/6] Hugo 发布失败（非关键）: {result.stderr[:200]}")
        else:
            log(f"[3e/6] 警告: monitor_upload.sh 不存在，跳过")
        
        log(f"=" * 60)
        log(f"[OK] 视频 {video_id} 处理完成！")
        log(f"=" * 60)
        return True
        
    except Exception as e:
        log(f"[ERROR] 处理视频 {video_id} 失败: {e}")
        return False

def main():
    """主函数"""
    log("=" * 60)
    log("YouTube 视频自动处理管道启动")
    log("=" * 60)
    
    # 切换到工作目录
    os.chdir(WORK_DIR)
    log(f"工作目录: {WORK_DIR}")
    
    # 读取 last_video.txt
    last_video_file = WORK_DIR / "last_video.txt"
    if last_video_file.exists():
        last_video_id = last_video_file.read_text(encoding='utf-8').strip()
        log(f"上次处理的视频: {last_video_id}")
    else:
        last_video_id = None
        log(f"首次运行（last_video.txt 不存在）")
    
    # 获取最近3个视频
    log(f"获取最近3个视频...")
    cmd = f'yt-dlp --flat-playlist -J "{CHANNEL_URL}"'
    output = run_cmd(cmd)
    
    try:
        data = json.loads(output)
        videos = data['entries'][:3]  # 只取前3个
    except Exception as e:
        log(f"[ERROR] 解析视频列表失败: {e}")
        return
    
    log(f"获取到 {len(videos)} 个视频")
    
    # 检查哪些视频需要处理
    videos_to_process = []
    for video in videos:
        video_id = video['id']
        title = video.get('title', 'N/A')
        
        if video_id != last_video_id:
            videos_to_process.append((video_id, title))
        else:
            # 已经处理到最后一个，后面的不需要处理
            break
    
    if not videos_to_process:
        log(f"[OK] 没有新视频需要处理")
        return
    
    log(f"发现 {len(videos_to_process)} 个新视频需要处理")
    
    # 按顺序处理（从旧到新）
    success_count = 0
    for video_id, title in reversed(videos_to_process):
        if process_video(video_id, title):
            success_count += 1
    
    log("=" * 60)
    log(f"处理完成！成功: {success_count}/{len(videos_to_process)}")
    log("=" * 60)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log(f"[ERROR] 主函数异常: {e}")
        sys.exit(1)
