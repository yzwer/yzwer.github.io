#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查 @sunriches 频道是否有新视频
"""
import json
import os
import sys

WORK_DIR = r'C:\Users\11132\.qclaw\workspace-yw3plsutb1jupnif\youtube_videos'
CHANNEL_URL = "https://www.youtube.com/@sunriches/videos"
LAST_VIDEO_FILE = os.path.join(WORK_DIR, 'last_video.txt')

print('[1/5] 读取上次处理的视频ID...')

# 读取上次处理的视频ID
try:
    if os.path.exists(LAST_VIDEO_FILE):
        with open(LAST_VIDEO_FILE, 'r') as f:
            last_vid = f.read().strip()
        print(f'OK: 上次处理: {last_vid}')
    else:
        last_vid = ''
        print('INFO: 首次运行，无历史记录')
except Exception as e:
    print(f'ERROR: 读取失败: {e}')
    sys.exit(1)

print('\n[2/5] 获取 @sunriches 最新视频列表...')

# 使用 yt-dlp 获取最新视频
try:
    import subprocess
    
    # 重试3次
    for attempt in range(1, 4):
        print(f'  尝试 {attempt}/3...')
        try:
            cmd = [
                'yt-dlp',
                '--flat-playlist',
                '-J',
                CHANNEL_URL
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30,
                cwd=WORK_DIR
            )
            
            if result.returncode == 0:
                data = json.loads(result.stdout)
                entries = data.get('entries', [])
                
                if not entries:
                    print('ERROR: 未获取到视频列表')
                    sys.exit(1)
                
                # 获取最新视频ID
                latest_vid = entries[0].get('id', '')
                latest_title = entries[0].get('title', 'N/A')
                
                print(f'OK: 最新视频: {latest_vid}')
                print(f'    标题: {latest_title}')
                print(f'    前3个视频:')
                for i, entry in enumerate(entries[:3]):
                    print(f'      {i+1}. {entry.get("id", "")} - {entry.get("title", "N/A")}')
                
                break
                
            else:
                print(f'ERROR: yt-dlp 失败: {result.stderr}')
                if attempt < 3:
                    import time
                    wait_time = [5, 15, 30][attempt - 1]
                    print(f'  {wait_time}秒后重试...')
                    time.sleep(wait_time)
                else:
                    print('ERROR: 3次尝试均失败')
                    sys.exit(1)
                    
        except Exception as e:
            print(f'ERROR: 尝试 {attempt} 失败: {e}')
            if attempt < 3:
                import time
                wait_time = [5, 15, 30][attempt - 1]
                print(f'  {wait_time}秒后重试...')
                time.sleep(wait_time)
            else:
                print('ERROR: 3次尝试均失败')
                sys.exit(1)
    
except Exception as e:
    print(f'ERROR: 获取最新视频失败: {e}')
    sys.exit(1)

print('\n[3/5] 对比判断...')

if latest_vid == last_vid:
    print('INFO: 无新视频')
    print('=' * 60)
    print('📭 今日检查 @sunriches 频道，暂无新视频发布。')
    print('=' * 60)
    sys.exit(0)  # 正常退出，无新视频
else:
    print(f'NEW: 发现新视频！')
    print(f'      旧: {last_vid}')
    print(f'      新: {latest_vid}')
    print('=' * 60)
    print(f'ACTION: 开始自动处理 {latest_vid}')
    print('=' * 60)
    
    # 输出新视频ID，供后续步骤使用
    print(f'\n>>> NEW_VIDEO_FOUND:{latest_vid}')
    print(f'>>> VIDEO_TITLE:{latest_title}')

print('\n=== 检查完成 ===')
