# -*- coding: utf-8 -*-
"""Generate WeChat article for RYq2pdfv8l0 - North Korea constitutional amendments"""
import json, os

base = os.path.dirname(os.path.abspath(__file__))
vid = 'RYq2pdfv8l0'
out = os.path.join(base, f'{vid}_wechat_article.html')

with open(os.path.join(base, f'{vid}.json'), 'r', encoding='utf-8') as f:
    d = json.load(f)
text = d.get('text', '')

# Full article content
title = "金正恩大动作：朝鲜修