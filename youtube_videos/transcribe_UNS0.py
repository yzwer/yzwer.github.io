#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Whisper 转录 - UNS0C52hnJI
"""
import whisper
import os
import sys

VID = "UNS0C52hnJI"
WORK_DIR = r'C:\Users\11132\.qclaw\workspace-yw3plsutb1jupnif\youtube_videos'

print(f'[3b/5] 开始 Whisper 转录: {VID}')

# 检查视频文件
video_path = os.path.join(WORK_DIR, f'{VID}.mp4')
if not os.path.exists(video_path):
    print(f'ERROR: 视频文件不存在: {video_path}')
    sys.exit(1)

print(f'OK: 视频文件存在: {video_path}')

# 提取音频
audio_path = os.path.join(WORK_DIR, f'{VID}.wav')
print(f'\n[1/2] 提取音频...')

if not os.path.exists(audio_path):
    print(f'  使用 ffmpeg 提取音频...')
    import subprocess
    
    cmd = [
        'ffmpeg', '-i', video_path,
        '-vn', '-acodec', 'pcm_s16le',
        '-ar', '16000', '-ac', '1',
        audio_path, '-y'
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    
    if result.returncode != 0:
        print(f'ERROR: ffmpeg 失败: {result.stderr}')
        sys.exit(1)
    
    print(f'OK: 音频提取成功: {audio_path}')
else:
    print(f'INFO: 音频已存在，跳过提取')

# Whisper 转录
print(f'\n[2/2] Whisper 转录...')
print(f'  模型: base')
print(f'  语言: zh (中文)')

try:
    model = whisper.load_model("base")
    print(f'  OK: 模型加载成功')
    
    result = model.transcribe(audio_path, language="zh")
    print(f'  OK: 转录完成')
    
    # 保存 JSON
    import json
    
    output_path = os.path.join(WORK_DIR, f'{VID}.json')
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    # 统计
    segments = result.get('segments', [])
    text_length = len(result.get('text', ''))
    
    print(f'  OK: JSON 已保存: {output_path}')
    print(f'  段落数: {len(segments)}')
    print(f'  文本长度: {text_length} 字符')
    
except Exception as e:
    print(f'ERROR: 转录失败: {e}')
    sys.exit(1)

print('\n=== 转录完成 ===')
print(f'输出文件: {output_path}')
print(f'文本预览: {result.get("text", "")[:100]}...')
