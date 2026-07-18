#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量上传积压的公众号草稿
避免PowerShell语法问题，纯Python实现
"""
import os
import sys
import subprocess

WORK_DIR = r'C:\Users\11132\.qclaw\workspace-yw3plsutb1jupnif\youtube_videos'

# 待上传的视频ID列表（按时间顺序）
VIDEOS = [
    'o-S-ibIBvrk',
    '_gn03Q1qxtw',
    'ExxZ-ug-LFs',
    'RYq2pdfv8l0',
    's_MKH36lhgg',
    'f-uXjRn19uU',
    '1OEIQTj_5QY',
    'JCyCN9x0JEc',
    'eONVYvBxkyQ',
    'oDq9hCzzEng',
    '_260064XYuQ'
]

def log(msg):
    print(msg, flush=True)

def upload_video(vid):
    """上传单个视频的草稿"""
    log(f"\n{'='*70}")
    log(f"处理: {vid}")
    log(f"{'='*70}")
    
    # 检查HTML文件是否存在
    html_path = os.path.join(WORK_DIR, f'{vid}_wechat_article.html')
    if not os.path.exists(html_path):
        log(f"[ERROR] HTML文件不存在: {html_path}")
        return False
    
    # 调用upload_draft.py
    cmd = f'python "{os.path.join(WORK_DIR, "upload_draft.py")}" "{vid}"'
    log(f"命令: {cmd[:80]}...")
    
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=300,
            cwd=WORK_DIR
        )
        
        # 打印输出
        if result.stdout:
            for line in result.stdout.split('\n'):
                if line.strip():
                    log(line)
        
        if result.returncode == 0:
            log(f"[OK] {vid} 上传成功")
            return True
        else:
            log(f"[ERROR] {vid} 上传失败 (返回码: {result.returncode})")
            if result.stderr:
                for line in result.stderr.split('\n')[:10]:
                    if line.strip():
                        log(f"  ERR: {line}")
            return False
            
    except subprocess.TimeoutExpired:
        log(f"[ERROR] {vid} 超时")
        return False
    except Exception as e:
        log(f"[ERROR] {vid} 异常: {e}")
        return False

def main():
    log("=" * 70)
    log("批量上传公众号草稿")
    log("=" * 70)
    log(f"待上传数量: {len(VIDEOS)}")
    log(f"当前目录: {WORK_DIR}")
    
    success_count = 0
    fail_count = 0
    ip_whitelist_error = False
    
    for i, vid in enumerate(VIDEOS, 1):
        log(f"\n[{i}/{len(VIDEOS)}] {vid}")
        if upload_video(vid):
            success_count += 1
        else:
            fail_count += 1
            # 检查是否是IP白名单错误
            # (通过检查输出或文件日志)
    
    log("\n" + "=" * 70)
    log(f"完成！成功: {success_count}, 失败: {fail_count}")
    log("=" * 70)
    
    if fail_count > 0:
        log("\n[提示] 如果失败原因是IP白名单错误 (errcode 40164):")
        log("  1. 登录 https://mp.weixin.qq.com")
        log("  2. 设置与开发 → 基本配置 → IP白名单")
        log(f"  3. 添加当前出口IP (可通过 https://api.ipify.org 查询)")
        log("\n或者运行: python -c \"import requests; print('IP:', requests.get('https://api.ipify.org').text)\"")
    
    return 0 if fail_count == 0 else 1

if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        log("\n[WARNING] 用户中断")
        sys.exit(1)
    except Exception as e:
        log(f"[ERROR] 未捕获的异常: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
