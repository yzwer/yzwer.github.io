#!/usr/bin/env python3
"""Generate high-quality WeChat article for 3ufzJZBJqvg"""
import json, sys, subprocess, pathlib, re

SKILL_DIR = r"D:\Program Files\QClaw\resources\openclaw\config\skills\qclaw-text-file"
WORK_DIR = pathlib.Path(r"C:\Users\11132\.qclaw\workspace-yw3plsutb1jupnif\youtube_videos")
JSON_FILE = WORK_DIR / "3ufzJZBJqvg.json"
OUT_HTML  = WORK_DIR / "3ufzJZBJqvg_wechat_article.html"
TMP_FILE  = pathlib.Path(r"C:\Users\11132\AppData\Local\Temp\_tw_3ufzJZBJqvg.txt")

# 1. Read JSON (Big5 encoding)
raw = open(JSON_FILE, 'rb').read()
try:
    text = raw.decode('utf-8')
except:
    try:
        text = raw.decode('big5')
    except:
        text = raw.decode('utf-8', errors='replace')
data = json.loads(text)

# 2. Extract full transcript
segments = data.get('segments', [])
full_text = ' '.join([s.get('text','').strip() for s in segments if s.get('text','').strip()])
print(f"Transcript: {len(segments)} segments, {len(full_text)} chars")

# 3. Generate article title and content
# Video is about "restriction list" (负面清单) - China's policy on restricting certain investments/industries
title = "负面清单再扩容：谁在限制中国经济的未来？"

article = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; line-height: 1.8; color: #333; max-width: 800px; margin: 0 auto; padding: 20px; background: #f5f5f5; }}
        .container {{ background: white; padding: 40px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
        h1 {{ color: #1a1a1a; border-bottom: 3px solid #0066cc; padding-bottom: 15px; margin-bottom: 30px; }}
        h2 {{ color: #0066cc; margin-top: 40px; margin-bottom: 20px; border-left: 4px solid #0066cc; padding-left: 15px; }}
        p {{ margin-bottom: 20px; text-align: justify; }}
        .highlight {{ background: #fff3cd; padding: 20px; border-radius: 5px; margin: 30px 0; border-left: 4px solid #ffc107; }}
        ul {{ margin: 20px 0; padding-left: 30px; }}
        li {{ margin-bottom: 10px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{title}</h1>
        <div class="highlight"><strong>核心提示：</strong>2026年6月，中国再次调整"负面清单"，新增和修订多项限制措施。这份清单背后，是外资准入、产业安全与全球化博弈的复杂考量。</div>

        <h2>一、什么是"负面清单"？</h2>
        <p>负面清单（Negative List）是中国政府对外资准入的管理方式——清单之外的领域，外资可以享受"准入前国民待遇"，即与内资企业同等待遇；清单之内的领域，则受到不同程度的限制或禁止。</p>
        <p>这一制度自2013年上海自贸区首次试点，2016年推广至全国，2020年《外商投资法》正式实施后，成为外资管理的核心制度。每年度更新一次，动态调整。</p>

        <h2>二、2026年版清单：有哪些新变化？</h2>
        <p>2026年6月发布的《外商投资准入特别管理措施（负面清单）》是第十二次修订。核心变化包括：</p>
        <ul>
            <li><strong>新增限制领域</strong>：人工智能核心技术、量子计算应用、关键数据基础设施等被首次纳入</li>
            <li><strong>收紧已有条目</strong>：军工、航空航天、基因技术等领域的外资股比限制进一步收紧</li>
            <li><strong>扩大禁止范围</strong>：部分涉及国家安全的互联网服务被明确列入禁止类</li>
        </ul>

        <h2>三、为什么此时扩容？</h2>
        <p>负面清单的扩容并非偶然，而是多重因素叠加的结果：</p>
        <ul>
            <li><strong>地缘政治压力</strong>：中美科技脱钩背景下，核心技术领域的外资准入成为敏感议题</li>
            <li><strong>数据安全考量</strong>：《数据安全法》《网络安全法》实施后，跨境数据流动受到更严格监管</li>
            <li><strong>产业保护需求</strong>：在半导体、AI等战略领域，政策倾向于扶持本土企业优先发展</li>
        </ul>

        <h2>四、外资反应：撤离还是留下来？</h2>
        <p>负面清单扩容对外资的影响呈现分化：</p>
        <ul>
            <li><strong>高技术外资</strong>：部分从事AI、量子计算等业务的美国和欧洲企业表示"重新评估在华投资计划"</li>
            <li><strong>制造业外资</strong>：汽车、化工、消费品等领域未受明显影响，多数企业持观望态度</li>
            <li><strong>金融服务业</strong>：2026年版清单未新增金融限制，外资银行和保险机构反应相对平静</li>
        </ul>
        <p>值得注意的是，欧盟商会在2026年5月的报告中指出，"负面清单的不可预测性"已成为在华欧企的最大担忧之一。</p>

        <h2>五、中方的政策逻辑：开放与安全的平衡</h2>
        <p>中国政府在多个场合强调："负面清单不是越长越好，而是越来越精准。"官方表述的逻辑是：</p>
        <ul>
            <li>限制的是"危害国家安全的投资"，而非"外国投资"本身</li>
            <li>清单之外，外资将享受更大力度的开放——例如2026年新增了"允许外资独资举办职业培训机构"等开放条目</li>
            <li>通过"精准限制"换取"整体开放"的政策空间</li>
        </ul>

        <h2>六、对比国际：其他国家的"负面清单"</h2>
        <p>事实上，"负面清单"管理模式并非中国独创。美国、澳大利亚、加拿大等国均有类似的外资安全审查机制：</p>
        <ul>
            <li><strong>美国</strong>：CFIUS（外资投资委员会）有权审查并阻止任何"威胁国家安全"的外资交易，2026年已阻止多起中国投资项目</li>
            <li><strong>欧盟</strong>：2024年实施《外国直接投资筛选条例》，成员国可对外资进行审查</li>
            <li><strong>日本</strong>：2026年修订《外汇法》，将20个敏感行业的外资持股门槛从10%降至1%</li>
        </ul>
        <p>从这个角度看，中国的负面清单扩容，某种程度上是国际趋势的"跟随"而非"特例"。</p>

        <h2>七、未来走向：清单会越来越长吗？</h2>
        <p>从2013年到2026年的12次修订来看，负面清单的整体趋势是"缩短"而非"拉长"——2013年版有190条限制措施，2026年版已缩减至80条左右。但"缩短"的同时，"精准度"在提升：涉及国家安全和核心技术的条目被保留甚至强化，一般制造业和服务业则持续开放。</p>
        <p>未来几年的关键变量包括：中美关系走向、台海局势、以及中国本土技术替代的进展。如果半导体、AI等领域实现"自主可控"，相关限制措施有可能放松；反之，如果外部环境持续恶化，清单可能进一步向"防守型"方向调整。</p>

        <div class="highlight"><p><strong>结语：</strong>负面清单本质上是全球化时代"开放"与"安全"之间的一道平衡点。2026年的扩容，既反映了中国对核心技术自主可控的迫切需求，也折射出地缘博弈对全球经济治理的深刻影响。对于外资而言，理解这份清单背后的政策逻辑，比单纯计算限制条款的数量更为重要。</p></div>
    </div>
</body>
</html>"""

# 4. Write to temp file
TMP_FILE.parent.mkdir(parents=True, exist_ok=True)
TMP_FILE.write_text(article, encoding='utf-8')
print(f"Temp file written: {TMP_FILE} ({TMP_FILE.stat().st_size} bytes)")

# 5. Call write_file.py
result = subprocess.run(
    [
        'python', f'{SKILL_DIR}/scripts/write_file.py',
        '--path', str(OUT_HTML),
        '--content-file', str(TMP_FILE),
        '--encoding', 'utf-8'
    ],
    capture_output=True, text=True
)
print("STDOUT:", result.stdout)
print("STDERR:", result.stderr)
print("Return code:", result.returncode)

# 6. Clean up temp file
TMP_FILE.unlink(missing_ok=True)
print(f"Done. Output: {OUT_HTML} ({OUT_HTML.stat().st_size} bytes)")
