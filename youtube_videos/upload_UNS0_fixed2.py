#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
上传 UNS0C52hnJI 文章到公众号草稿箱 - 修复 draft/add API 响应处理
自动执行，不停止！
"""
import os
import sys
import requests
import json
import time

VID = "UNS0C52hnJI"
WORK_DIR = r'C:\Users\11132\.qclaw\workspace-yw3plsutb1jupnif\youtube_videos'
APPID = 'wxabc1784dbf87c3de'
APPSECRET = '10d4335f33efcb36d3f27551870595d5'

print('[3d/5] 上传公众号草稿箱（修复版）')
print(f'VID: {VID}')

# 1. 获取 access_token
print('\n[1/3] 获取 access_token...')
token_url = f'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APPID}&secret={APPSECRET}'

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

# 2. 上传封面图
print('\n[2/3] 上传封面图...')
cover_path = os.path.join(WORK_DIR, 'frame_10pct.jpg')

if not os.path.exists(cover_path):
    print(f'  ERROR: 封面图不存在: {cover_path}')
    sys.exit(1)

# 上传封面（禁用代理）
with open(cover_path, 'rb') as f:
    cover_data = f.read()

upload_url = f'https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={access_token}&type=thumb'
files = {'media': (os.path.basename(cover_path), cover_data, 'image/jpeg')}

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

# 3. 创建草稿（禁用代理，重试3次）
print('\n[3/3] 创建草稿...')
article_path = os.path.join(WORK_DIR, f'{VID}_wechat_article.html')
with open(article_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 构造草稿数据
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

# 调用 API（禁用代理）
draft_url = f'https://api.weixin.qq.com/cgi-bin/draft/add?access_token={access_token}'
headers = {'Content-Type': 'application/json; charset=utf-8'}

for attempt in range(3):
    try:
        resp = requests.post(draft_url, data=json.dumps(draft_data, ensure_ascii=False).encode('utf-8'), headers=headers, timeout=30, proxies={'http': None, 'https': None})
        result = resp.json()
        
        # 关键修复：draft/add API 成功时直接返回 media_id，不返回 errcode
        if 'media_id' in result:
            media_id = result['media_id']
            print(f'  OK: 草稿创建成功! (尝试 {attempt+1})')
            print(f'   media_id = {media_id}')
            
            # 更新 last_video.txt
            with open(os.path.join(WORK_DIR, 'last_video.txt'), 'w') as f:
                f.write(VID)
            print(f'  OK: last_video.txt 已更新: {VID}')
            
            print('\n=== 发布成功 ===')
            print(f'>>> SUCCESS:{VID}:{media_id}')
            break
        elif result.get('errcode', 0) != 0:
            print(f'  尝试 {attempt+1} 失败: {result}')
            if attempt == 2:
                print(f'  ERROR: 草稿创建失败 after 3 attempts')
                sys.exit(1)
            time.sleep(10)
        else:
            # 未知响应格式
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

print('\n✅ 任务完成！')
