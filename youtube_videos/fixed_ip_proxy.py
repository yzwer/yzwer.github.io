#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
固定IP代理中间件
让微信API请求走固定IP代理，解决IP白名单动态变化问题
"""

import os
import sys
import json
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# 配置：您的固定IP代理地址（需要您提供一个固定IP的代理）
# 格式: "http://username:password@fixed-ip-proxy:port"
# 如果没有，可以使用Cloudflare Workers（免费）或固定IP VPS
PROXY_URL = os.getenv('WECHAT_PROXY_URL', None)  # 设置为None则直接使用当前IP

WECHAT_API_BASE = 'https://api.weixin.qq.com'

@app.route('/wechat/<path:subpath>', methods=['GET', 'POST'])
def proxy_wechat_api(subpath):
    """代理微信API请求"""
    target_url = f"{WECHAT_API_BASE}/{subpath}"
    
    # 准备请求
    headers = {key: value for key, value in request.headers if key != 'Host'}
    params = request.args.to_dict()
    data = request.get_data() if request.method == 'POST' else None
    
    # 发送请求（通过代理或直接）
    proxies = {'https': PROXY_URL, 'http': PROXY_URL} if PROXY_URL else None
    
    try:
        resp = requests.request(
            method=request.method,
            url=target_url,
            headers=headers,
            params=params,
            data=data,
            proxies=proxies,
            timeout=30
        )
        
        # 返回响应
        return (resp.content, resp.status_code, resp.headers.items())
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_current_ip():
    """获取当前出口IP"""
    try:
        return requests.get('https://api.ipify.org', timeout=5).text
    except:
        return 'unknown'

if __name__ == '__main__':
    print("=" * 70)
    print("微信API固定IP代理服务")
    print("=" * 70)
    print(f"当前出口IP: {get_current_ip()}")
    print(f"代理模式: {'启用' if PROXY_URL else '禁用（直接使用当前IP）'}")
    print(f"监听地址: http://0.0.0.0:8080")
    print("=" * 70)
    print("\n使用方法:")
    print("1. 设置环境变量 WECHAT_PROXY_URL 为您的固定IP代理地址")
    print("2. 修改 upload_draft.py，将API地址改为 http://localhost:8080/wechat/...")
    print("3. 启动此服务: python fixed_ip_proxy.py")
    print("4. 添加 当前出口IP 到微信公众平台IP白名单")
    print("\n提示: 如果没有固定IP代理，此方法无法解决IP白名单问题")
    print("建议使用方案B（手动上传）或方案C（VPS固定IP）")
    print("=" * 70)
    
    app.run(host='0.0.0.0', port=8080, debug=False)
