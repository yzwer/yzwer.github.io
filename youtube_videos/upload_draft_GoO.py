#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
上传 GoO-MQcVnI8 文章到公众号草稿箱
"""
import requests
import json
import os

VID = "GoO-MQcVnI8"
APPID = "wxabc1784dbf87c3de"
APPSECRET = "10d4335f33efcb36d3f27551870595d5"
ARTICLE_PATH = r'C:\Users\11132\.qclaw\workspace-yw3plsutb1jupnif\youtube_videos\GoO-MQcVnI8_wechat_article.html'
VIDEO_PATH = r'C:\Users\11132\.qclaw\workspace-yw3plsutb1jupnif\youtube_videos\GoO-MQcVnI8.mp4'

print('[1/4] 获取 access_token...')
try:
    token_url = f'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APPID}&secret={APPSECRET}'
    token_resp = requests.get(token_url, timeout=10)
    token_data = token_resp.json()
    
    if 'access_token' not in token_data:
        print(f'ERROR: 获取 token 失败: {token_data}')
        exit(1)
    
    ACCESS_TOKEN = token_data['access_token']
    print(f'OK: token 获取成功')
except Exception as e:
    print(f'ERROR: {e}')
    exit(1)

print('\n[2/4] 上传封面图...')
try:
    # 从视频截取封面
    cover_path = r'C:\Users\11132\.qclaw\workspace-yw3plsutb1jupnif\youtube_videos\GoO_cover.jpg'
    
    # 使用 ffmpeg 截取
    import subprocess
    cmd = [
        'ffmpeg', '-i', VIDEO_PATH,
        '-ss', '00:00:30',
        '-vframes', '1',
        cover_path, '-y'
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if not os.path.exists(cover_path):
        print(f'WARNING: 封面截取失败，尝试使用第一帧...')
        cmd = ['ffmpeg', '-i', VIDEO_PATH, '-ss', '00:00:05', '-vframes', '1', cover_path, '-y']
        result = subprocess.run(cmd, capture_output=True, text=True)
    
    if os.path.exists(cover_path):
        # 上传封面
        upload_url = f'https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={ACCESS_TOKEN}&type=image'
        with open(cover_path, 'rb') as f:
            files = {'media': f}
            upload_resp = requests.post(upload_url, files=files, timeout=30)
            upload_data = upload_resp.json()
        
        if 'media_id' in upload_data:
            thumb_media_id = upload_data['media_id']
            print(f'OK: 封面上传成功: {thumb_media_id}')
        else:
            print(f'WARNING: 封面上传失败: {upload_data}')
            thumb_media_id = ''
    else:
        print(f'WARNING: 封面文件不存在，将不使用封面')
        thumb_media_id = ''
except Exception as e:
    print(f'WARNING: 封面上传失败: {e}')
    thumb_media_id = ''

print('\n[3/4] 读取文章内容...')
try:
    with open(ARTICLE_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
    print(f'OK: 文章读取成功 ({len(content)} 字符)')
except Exception as e:
    print(f'ERROR: 读取文章失败: {e}')
    exit(1)

print('\n[4/4] 创建草稿...')
try:
    # 构造草稿数据
    draft_data = {
        "articles": [
            {
                "title": "特朗普访华拿到什么？普京紧急跟进：中美俄三角关系正在重写",
                "author": "AI 自动生成",
                "digest": "特朗普刚结束北京之行，普京就紧急访华。中美达成波音订单、农产品采购、机制建设等成果，但芯片、台湾等核心矛盾未解。",
                "content": content,
                "content_source_url": "",
                "thumb_media_id": thumb_media_id,
                "need_open_comment": 0,
                "only_fans_can_comment": 0
            }
        ]
    }
    
    # 调用 API
    draft_url = f'https://api.weixin.qq.com/cgi-bin/draft/add?access_token={ACCESS_TOKEN}'
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    resp = requests.post(draft_url, data=json.dumps(draft_data, ensure_ascii=False).encode('utf-8'), headers=headers, timeout=30)
    result = resp.json()
    
    if result.get('errcode', 0) == 0:
        media_id = result.get('media_id', '')
        print(f'OK: 草稿创建成功!')
        print(f'    media_id = {media_id}')
        
        # 更新 last_video.txt
        with open(r'C:\Users\11132\.qclaw\workspace-yw3plsutb1jupnif\youtube_videos\last_video.txt', 'w') as f:
            f.write(VID)
        print(f'OK: last_video.txt 已更新: {VID}')
        
    else:
        print(f'ERROR: 草稿创建失败: {result}')
        exit(1)
        
except Exception as e:
    print(f'ERROR: 创建草稿失败: {e}')
    exit(1)

print('\n=== 全部完成 ===')
print(f'视频ID: {VID}')
print(f'草稿 media_id: {media_id}')
print('请去微信公众平台草稿箱查看！')
