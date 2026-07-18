#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
upload_draft.py
上传公众号文章草稿
用法: python upload_draft.py <video_id>
"""
import os
import sys
import requests
import json
import subprocess
import time

# 配置
WORK_DIR = r'C:\Users\11132\.qclaw\workspace-yw3plsutb1jupnif\youtube_videos'
APPID = 'wxabc1784dbf87c3de'
APPSECRET = '10d4335f33efcb36d3f27551870595d5'

# 强制使用代理（确保IP一致）
PROXIES = {
    'http': 'socks5://127.0.0.1:6789',
    'https': 'socks5://127.0.0.1:6789'
}


def log(msg):
    print(msg, flush=True)


def get_access_token():
    """获取 access_token"""
    url = f'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APPID}&secret={APPSECRET}'
    
    for attempt in range(3):
        try:
            # 强制走代理，确保IP一致
            resp = requests.get(url, timeout=10, proxies=PROXIES)
            result = resp.json()
            if 'access_token' in result:
                return result['access_token']
            else:
                log(f'  [ERROR] 获取token失败: {result}')
                if attempt < 2:
                    time.sleep(5)
        except Exception as e:
            log(f'  [ERROR] 请求异常: {e}')
            if attempt < 2:
                time.sleep(5)
    
    return None


def extract_cover(vid):
    """用 ffmpeg 提取封面"""
    cover_path = os.path.join(WORK_DIR, f'{vid}_cover.jpg')
    video_path = os.path.join(WORK_DIR, f'{vid}.mp4')
    
    if os.path.exists(cover_path):
        log(f'  [OK] 封面已存在: {os.path.basename(cover_path)}')
        return cover_path
    
    log(f'  提取封面中...')
    cmd = f'ffmpeg -i "{video_path}" -ss 00:00:30 -vframes 1 "{cover_path}" -y'
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
        if os.path.exists(cover_path):
            log(f'  [OK] 封面提取成功: {os.path.basename(cover_path)}')
            return cover_path
        else:
            log(f'  [ERROR] ffmpeg失败')
            return None
    except Exception as e:
        log(f'  [ERROR] {e}')
        return None


def upload_thumb(access_token, cover_path):
    """上传封面图"""
    url = f'https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={access_token}&type=thumb'
    
    with open(cover_path, 'rb') as f:
        cover_data = f.read()
    
    files = {'media': (os.path.basename(cover_path), cover_data, 'image/jpeg')}
    
    for attempt in range(3):
        try:
            # 强制走代理
            resp = requests.post(url, files=files, timeout=30, proxies=PROXIES)
            result = resp.json()
            if 'media_id' in result:
                log(f'  [OK] 封面上传成功: {result["media_id"]}')
                return result['media_id']
            else:
                log(f'  [ERROR] 封面上传失败: {result}')
                if attempt < 2:
                    time.sleep(5)
        except Exception as e:
            log(f'  [ERROR] 请求异常: {e}')
            if attempt < 2:
                time.sleep(5)
    
    return None


def create_draft(access_token, vid, thumb_media_id, title, content):
    """创建草稿"""
    url = f'https://api.weixin.qq.com/cgi-bin/draft/add?access_token={access_token}'
    
    articles = [{
        "title": truncate_by_bytes(title, 60),
        "author": "",
        "content": content,
        "digest": content[:120],
        "thumb_media_id": thumb_media_id,
        "content_source_url": "",
        "show_cover_pic": 1
    }]
    
    for attempt in range(3):
        try:
            # 强制走代理
            resp = requests.post(url, json={"articles": articles}, timeout=30, proxies=PROXIES)
            result = resp.json()
            if 'media_id' in result:
                log(f'  [OK] 草稿创建成功: {result["media_id"]}')
                return result['media_id']
            else:
                log(f'  [ERROR] 草稿创建失败: {result}')
                if attempt < 2:
                    time.sleep(5)
        except Exception as e:
            log(f'  [ERROR] 请求异常: {e}')
            if attempt < 2:
                time.sleep(5)
    
    return None


def truncate_by_bytes(text, max_bytes=60):
    """按UTF-8字节长度截断字符串"""
    encoded = text.encode('utf-8')
    if len(encoded) <= max_bytes:
        return text
    # 逐字符截断，确保不切断多字节字符
    result = ''
    for ch in text:
        if len((result + ch).encode('utf-8')) > max_bytes:
            break
        result += ch
    return result


def main():
    if len(sys.argv) < 2:
        print("用法: python upload_draft.py <video_id>")
        sys.exit(1)
    
    vid = sys.argv[1]
    article_path = os.path.join(WORK_DIR, f'{vid}_wechat_article.html')
    
    log(f'[{vid}] 开始上传公众号草稿...')
    
    # 检查文章文件
    if not os.path.exists(article_path):
        log(f'  [ERROR] 文章文件不存在: {article_path}')
        sys.exit(1)
    
    # 读取文章内容
    with open(article_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取标题
    import re
    title_match = re.search(r'<title>([^<]+)</title>', content)
    title = title_match.group(1) if title_match else f'视频内容_{vid}'[:64]
    log(f'  标题: {title}')
    
    # 步骤1: 提取封面
    log(f'\n[步骤1/3] 提取封面图...')
    cover_path = extract_cover(vid)
    if not cover_path:
        log('  [ERROR] 封面提取失败')
        sys.exit(1)
    
    # 步骤2: 获取 token
    log(f'\n[步骤2/3] 获取 access_token...')
    access_token = get_access_token()
    if not access_token:
        log('  [ERROR] 获取token失败')
        sys.exit(1)
    log(f'  [OK] token获取成功')
    
    # 步骤3: 上传封面
    log(f'\n[步骤3a/3] 上传封面图...')
    thumb_media_id = upload_thumb(access_token, cover_path)
    if not thumb_media_id:
        log('  [ERROR] 封面上传失败')
        sys.exit(1)
    
    # 步骤4: 创建草稿
    log(f'\n[步骤3b/3] 创建草稿...')
    media_id = create_draft(access_token, vid, thumb_media_id, title, content)
    if not media_id:
        log('  [ERROR] 草稿创建失败')
        sys.exit(1)
    
    log(f'\n====================')
    log(f'[OK] 全部完成!')
    log(f'  media_id: {media_id}')
    log(f'====================')


if __name__ == '__main__':
    main()
