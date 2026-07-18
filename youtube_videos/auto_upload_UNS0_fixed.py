#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整流程：提取封面 + 上传公众号草稿箱
修复：移除所有 emoji（PowerShell GBK 编码问题）
"""
import os
import sys
import requests
import json
import subprocess
import time

VID = "UNS0C52hnJI"
WORK_DIR = r'C:\Users\11132\.qclaw\workspace-yw3plsutb1jupnif\youtube_videos'
APPID = 'wxabc1784dbf87c3de'
APPSECRET = '10d4335f33efcb36d3f27551870595d5'

print('=' * 60)
print(f'[{VID}] 自动化流程开始')
print('=' * 60)

# ========== 步骤1: 提取封面图 ==========
print('\n[步骤1/4] 提取封面图...')
cover_path = os.path.join(WORK_DIR, f'{VID}_cover.jpg')
video_path = os.path.join(WORK_DIR, f'{VID}.mp4')

if not os.path.exists(cover_path):
    print(f'  封面不存在，用 ffmpeg 截取...')
    cmd = f'ffmpeg -i "{video_path}" -ss 00:00:30 -vframes 1 "{cover_path}" -y'
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        if os.path.exists(cover_path):
            print(f'  OK: 封面已提取: {os.path.basename(cover_path)}')
        else:
            print(f'  ERROR: ffmpeg 失败: {result.stderr[-200:]}')
            sys.exit(1)
    except Exception as e:
        print(f'  ERROR: {e}')
        sys.exit(1)
else:
    print(f'  OK: 封面已存在: {os.path.basename(cover_path)}')

# ========== 步骤2: 获取 access_token ==========
print('\n[步骤2/4] 获取 access_token...')
token_url = f'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APPID}&secret={APPSECRET}'

access_token = None
for attempt in range(3):
    try:
        resp = requests.get(token_url, timeout=10, proxies={'http': None, 'https': None})
        result = resp.json()
        if 'access_token' in result:
            access_token = result['access_token']
            print(f'  OK: token 获取成功 (尝试 {attempt+1})')
            break
        else:
            print(f'  尝试 {attempt+1} 失败: {result}')
            if attempt == 2:
                sys.exit(1)
            time.sleep(5)
    except Exception as e:
        print(f'  尝试 {attempt+1} 异常: {e}')
        if attempt == 2:
            sys.exit(1)
        time.sleep(5)

# ========== 步骤3: 上传封面图 ==========
print('\n[步骤3/4] 上传封面图...')
upload_url = f'https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={access_token}&type=thumb'

with open(cover_path, 'rb') as f:
    cover_data = f.read()

files = {'media': (os.path.basename(cover_path), cover_data, 'image/jpeg')}

thumb_media_id = None
for attempt in range(3):
    try:
        resp = requests.post(upload_url, files=files, timeout=30, proxies={'http': None, 'https': None})
        result = resp.json()
        if 'media_id' in result:
            thumb_media_id = result['media_id']
            print(f'  OK: 封面上传成功: {thumb_media_id} (尝试 {attempt+1})')
            break
        else:
            print(f'  尝试 {attempt+1} 失败: {result}')
            if attempt == 2:
                sys.exit(1)
            time.sleep(5)
    except Exception as e:
        print(f'  尝试 {attempt+1} 异常: {e}')
        if attempt == 2:
            sys.exit(1)
        time.sleep(5)

# ========== 步骤4: 创建草稿 ==========
print('\n[步骤4/4] 创建草稿...')
article_path = os.path.join(WORK_DIR, f'{VID}_wechat_article.html')
with open(article_path, 'r', encoding='utf-8') as f:
    content = f.read()

draft_data = {
    "articles": [
        {
            "title": "俄罗斯阅兵坦克去哪儿了？",
            "author": "",
            "digest": "2026年胜利日阅兵没有坦克，为什么？",
            "content": content,
            "content_source_url": "",
            "thumb_media_id": thumb_media_id,
            "need_open_comment": 0,
            "only_fans_can_comment": 0
        }
    ]
}

draft_url = f'https://api.weixin.qq.com/cgi-bin/draft/add?access_token={access_token}'
headers = {'Content-Type': 'application/json; charset=utf-8'}

for attempt in range(3):
    try:
        resp = requests.post(draft_url, data=json.dumps(draft_data, ensure_ascii=False).encode('utf-8'), headers=headers, timeout=30, proxies={'http': None, 'https': None})
        result = resp.json()
        
        # 关键：draft/add API 成功时直接返回 media_id
        if 'media_id' in result:
            media_id = result['media_id']
            print(f'  OK: 草稿创建成功! (尝试 {attempt+1})')
            print(f'   media_id = {media_id}')
            
            # 更新 last_video.txt
            with open(os.path.join(WORK_DIR, 'last_video.txt'), 'w') as f:
                f.write(VID)
            print(f'  OK: last_video.txt 已更新: {VID}')
            
            print('\n' + '=' * 60)
            print('任务完成！')
            print('=' * 60)
            print(f'>>> SUCCESS:{VID}:{media_id}')
            sys.exit(0)
        elif result.get('errcode', 0) != 0:
            print(f'  尝试 {attempt+1} 失败: {result}')
            if attempt == 2:
                print(f'  ERROR: 草稿创建失败 after 3 attempts')
                sys.exit(1)
            time.sleep(10)
        else:
            print(f'  尝试 {attempt+1} 未知响应: {result}')
            if attempt == 2:
                sys.exit(1)
            time.sleep(10)
    except Exception as e:
        print(f'  尝试 {attempt+1} 异常: {e}')
        if attempt == 2:
            print(f'  ERROR: 草稿创建失败 after 3 attempts')
            sys.exit(1)
        time.sleep(10)

print('ERROR: 不应该到达这里')
sys.exit(1)
