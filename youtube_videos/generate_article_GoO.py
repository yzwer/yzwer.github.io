#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成 GoO-MQcVnI8 公众号文章
从 Whisper JSON 提取内容，参考 sojKNj_uXYU 模板
"""
import json
import sys
import re

VID = "GoO-MQcVnI8"
JSON_PATH = rf'C:\Users\11132\.qclaw\workspace-yw3plsutb1jupnif\youtube_videos\{VID}.json'
OUTPUT_PATH = rf'C:\Users\11132\.qclaw\workspace-yw3plsutb1jupnif\youtube_videos\{VID}_wechat_article.html'

print('[1/3] 读取 Whisper 转录...')
try:
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(f'OK: 读取成功，文本段落数: {len(data.get("segments", []))}')
    print(f'    检测语言: {data.get("language", "unknown")}')
except Exception as e:
    print(f'ERROR: 读取失败: {e}')
    sys.exit(1)

# 提取完整文本
full_text = data.get('text', '')
if not full_text:
    # 从 segments 拼接
    segments = data.get('segments', [])
    full_text = ' '.join([s.get('text', '') for s in segments])

print(f'[2/3] 生成文章标题和章节...')
print(f'    文本长度: {len(full_text)} 字符')

# 基于内容提炼标题（不用原视频标题）
# 视频内容包含：特朗普访华、波音订单、芯片、普京访华
title = "特朗普访华拿到什么？普京紧急跟进：中美俄三角关系正在重写"

# 文章 HTML 模板（参考 sojKNj_uXYU_wechat_article.html 风格）
html_template = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            line-height: 1.8;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }}
        .container {{
            background: white;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #1a1a1a;
            border-bottom: 3px solid #0066cc;
            padding-bottom: 15px;
            margin-bottom: 30px;
        }}
        h2 {{
            color: #0066cc;
            margin-top: 40px;
            margin-bottom: 20px;
            border-left: 4px solid #0066cc;
            padding-left: 15px;
        }}
        p {{
            margin-bottom: 20px;
            text-align: justify;
        }}
        .highlight {{
            background: #fff3cd;
            padding: 20px;
            border-radius: 5px;
            margin: 30px 0;
            border-left: 4px solid #ffc107;
        }}
        .timeline {{
            background: #e7f3ff;
            padding: 20px;
            border-radius: 5px;
            margin: 30px 0;
        }}
        .footer {{
            margin-top: 50px;
            padding-top: 30px;
            border-top: 2px solid #eee;
            color: #666;
            font-size: 14px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{title}</h1>
        
        <div class="highlight">
            <strong>核心提示：</strong>特朗普刚结束北京之行，普京就紧急访华。中美达成波音订单、农产品采购、机制建设等成果，但芯片、台湾等核心矛盾未解。普京紧急跟进，背后有三重考量。
        </div>
        
        <h2>一、特朗普的"成果清单"</h2>
        <p>特朗普这次北京之行（5月13-15日），两国元首互动时间近9小时。他本人在空军1号上评价这是"非常成功的访问"，达成了"很多了不起的贸易协议"。</p>
        
        <h2>二、波音订单：200架的"初步承诺"</h2>
        <p>特朗普重点提及：中国同意购买200架波音飞机，后续可能追加到750架。波音公司确认了该信息。</p>
        <p>但需要注意：中方的表述相对低调。中国商务部公告提到"双方就中方向美方采购飞机...达成有关安排"，没有直接报200架这个数字。后续如何落地，还得看具体谈判。</p>
        
        <h2>三、农产品和能源：数十亿美元采购</h2>
        <p>中国会增加采购美国农产品，大豆、牛肉是重点。能源方面，石油和天然气也会多买些。特朗普说"期待美国农民从中受益"。</p>
        <p>中方公告也提到：推动解决农产品关税壁垒和市场准入问题，推动解决牛肉设施注册等问题。这些都是比较容易落地的。</p>
        
        <h2>四、机制建设：贸易理事会和投资理事会</h2>
        <p>双方同意成立贸易理事会和投资理事会。以后两国在贸易投资领域有什么分歧、有什么诉求，将通过这两个理事会来讨论，而不是直接互相对加关税。</p>
        <p>这个机制的建立，意味着中美以后有了一个正式的沟通渠道。从长远看，算是这次峰会比较扎实的一个成果。</p>
        
        <h2>五、芯片问题：H200没下单的背后</h2>
        <p>峰会期间有消息说，美国批准英伟达向中国科技企业出口芯片，每家最多7.5万个H200。但特朗普回国后透露："美国是批准出售了，但中国没有下单。"</p>
        <p>中国为啥没买？原因有几个：</p>
        <ul>
            <li><strong>价格贵</strong>：买H200要交25%的关税，性价比低。</li>
            <li><strong>技术迭代快</strong>：H200已经不是最顶级的了。英伟达下半年要量产新一代Rubin系列（R100），B200/B100才是现在真正的新王者。买H200，有点像买一个即将被取代的"旗舰"，有点亏。</li>
            <li><strong>国产替代</strong>：华为昇腾910C/910B、B2000、海光DCU、平头哥玄铁810、璧仞BR100这些国产芯片，表现都还不错。买H200，某种程度上是在帮英伟达清库存，还变相打压了国内芯片企业的市场空间。</li>
        </ul>
        
        <h2>六、台湾、霍尔木兹、AI安全</h2>
        <p>台湾问题：中方该说的都说了，重申了一贯立场。特朗普那边低调处理，白宫的表述是"双方重申各自立场"。</p>
        <p>霍尔木兹海峡：双方同意保持开放，能源通道不能出乱子。这背后涉及伊朗问题，两国在这个问题上有共同利益。</p>
        <p>AI安全：双方同意建立对话机制，以后在这个议题上保持沟通。</p>
        
        <h2>七、总体评价：降温稳局，有限突破</h2>
        <div class="timeline">
            <p><strong>一句话概括</strong>：降温稳局，谈点生意，没有翻天覆地的大突破。</p>
            <p>特朗普拿到了波音订单、农产品采购承诺，回去能跟选民说"创造了就业"，政治上有个交代。</p>
            <p>中国这边，接待规格给得很高，定调是"建设性战略稳定关系"，意思就是"互相尊重、有限竞争、别脱钩"，也算拿到了想要的稳定信号。</p>
            <p>但核心矛盾——例如科技封锁、台湾问题、贸易结构不平衡——一个都没真正解决。而且很多成果只是初步共识，历史上这种峰会后的承诺打折扣的情况挺常见的。</p>
            <p>后续谈判还会继续。9月份习近平可能访美，那时候又会是一个观察节点。</p>
        </div>
        
        <h2>八、普京紧急访华：三天够干什么？</h2>
        <p>特朗普前脚刚走，普京也要来了。北京时间5月18日晚间，中俄同时宣布：俄罗斯总统普京将于5月19日至20日对中国进行国事访问。</p>
        <p>有意思的是，普京这次是5月16日正式放出消息的，5月19日人就到了。中间多少时间呢？只有三天。一个大国领导人的国事访问，从宣布到成型也就三天。</p>
        <p>普通人出门旅游，收拾个行李、定个机票、规划一下路线，可能都不止这点时间。堂堂俄罗斯总统，一次正式国事访问搞得这么着急，似乎不太寻常。</p>
        
        <h2>九、普京为什么这么急？三种可能性</h2>
        
        <p><strong>第一种可能：来打听消息、探探口风</strong></p>
        <p>特朗普跟习近平谈了什么，公开的部分大家都知道：波音飞机、农产品贸易、理事会这些。但任何高级别会谈，真正重要的内容往往是在屏退记者之后，两个领导人一对一聊的那部分。这部分究竟聊了些什么，外人不知道，普京大概率也不知道。</p>
        <p>普京现在最怕的一件事，就是自己在这场中美博弈里变成了"筹码"。中国和美国在谈某些交易的时候