#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试微信API看到的IP地址"""
import requests
import json
import re

APPID = 'wxabc1784dbf87c3de'
APPSECRET = '10d4335f33efcb36d3f27551870595d5'

# 测试不同的代理配置
configs = [
    ("无代理", None),
    ("HTTP代理", {'http': 'http://127.0.0.1:6789', 'https': 'http://127.0.0.1:6789'}),
    ("SOCKS5代理", {'http': 'socks5://127.0.0.1:6789', 'https': 'socks5://127.0.0.1:6789'}),
]

url = f'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APPID}&secret={APPSECRET}'

print("=" * 70)
print("测试微信API看到的IP地址")
print("=" * 70)

for name, proxies in configs:
    print(f'\n[{name}]')
    print(f'  代理配置: {proxies}')
    
    try:
        resp = requests.get(url, timeout=10, proxies=proxies)
        result = resp.json()
        
        if 'errcode' in result and result['errcode'] == 40164:
            errmsg = result['errmsg']
            print(f'  响应: {errmsg}')
            
            # 提取IP
            ip_match = re.search(r'ip[^\d]*(\d+\.\d+\.\d+\.\d+)', errmsg)
            if ip_match:
                ip = ip_match.group(1)
                print(f'  *** 微信API看到的IP: {ip} ***')
            else:
                print(f'  无法提取IP')
        elif 'access_token' in result:
            print(f'  ✅ 成功获取token！IP白名单已生效')
        else:
            print(f'  未知响应: {result}')
            
    except Exception as e:
        print(f'  请求异常: {e}')

print("\n" + "=" * 70)
print("结论：")
print("1. 如果不同代理配置看到不同IP → 需要在代理软件中固定微信API的出口IP")
print("2. 如果看到相同IP → 直接将该IP添加到白名单")
print("=" * 70)
