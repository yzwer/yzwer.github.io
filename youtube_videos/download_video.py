#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
下载新视频 UNS0C52hnJI
"""
import subprocess
import os
import sys
import time

VID = "UNS0C52hnJI"
WORK_DIR = r'C:\Users\11132\.qclaw\workspace-yw3plsutb1jupnif\youtube_videos'

print(f'[2/5] 开始下载视频: {VID}')
print(f'    标题: Tanks too afraid to show up, what happened?')

# 检查是否已存在
output_path = os.path.join(WORK_DIR, f'{VID}.mp4')
if os.path.exists(output_path):
    print(f'INFO: 视频已存在，跳过下载')
    print(f'OK: {output_path}')
    sys.exit(0)

# 使用 yt-dlp 下载（重试3次）
for attempt in range(1, 4):
    print(f'  尝试 {attempt}/3...')
    try:
        cmd = [
            'yt-dlp',
            '-f', 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            '-o', f'{VID}.%(ext)s',
            '--merge-output-format', 'mp4',
            f'https://www.youtube.com/watch?v={VID}'
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300,
            cwd=WORK_DIR
        )
        
        if result.returncode == 0:
            # 检查文件是否生成
            if os.path.exists(output_path):
                file_size = os.path.getsize(output_path) / (1024 * 1024)
                print(f'OK: 下载成功!')
                print(f'    文件: {output_path}')
                print(f'    大小: {file_size:.1f} MB')
                sys.exit(0)
            else:
                # 可能文件名不同，查找匹配的文件
                for f in os.listdir(WORK_DIR):
                    if f.startswith(VID) and f.endswith('.mp4'):
                        file_size = os.path.getsize(os.path.join(WORK_DIR, f)) / (1024 * 1024)
                        print(f'OK: 下载成功!')
                        print(f'    文件: {f}')
                        print(f'    大小: {file_size:.1f} MB')
                        sys.exit(0)
                
                print(f'WARNING: 未找到输出文件，可能文件名不同')
                if attempt < 3:
                    wait_time = [5, 15, 30][attempt - 1]
                    print(f'  {wait_time}秒后重试...')
                    time.sleep(wait_time)
        else:
            print(f'ERROR: 下载失败: {result.stderr}')
            if attempt < 3:
                wait_time = [5, 15, 30][attempt - 1]
                print(f'  {wait_time}秒后重试...')
                time.sleep(wait_time)
            else:
                print('ERROR: 3次尝试均失败')
                sys.exit(1)
                
    except Exception as e:
        print(f'ERROR: 尝试 {attempt} 失败: {e}')
        if attempt < 3:
            wait_time = [5, 15, 30][attempt - 1]
            print(f'  {wait_time}秒后重试...')
            time.sleep(wait_time)
        else:
            print('ERROR: 3次尝试均失败')
            sys.exit(1)

print('ERROR: 下载失败')
sys.exit(1)
