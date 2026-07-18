# -*- coding: utf-8 -*-
"""Generate WeChat article for 4IIJY9Y5L54"""
import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')

base = r'C:\Users\11132\.qclaw\workspace-yw3plsutb1jupnif\youtube_videos'
vid = '4IIJY9Y5L54'
tmp_file = os.path.join(os.environ.get('TEMP','/tmp'), '_tw_4ij.html')

# Read full transcript for details
with open(os.path.join(base, f'{vid}.json'), 'r', encoding='utf-8') as f:
    d = json.load(f)
full_text = d.get('text', '')

# Read CSS from reference
ref_file = os.path.join(base, 'sojKNj_uXYU_wechat_article.html')
with open(ref_file, 'r', encoding='utf-8') as f:
    ref_html = f.read()
css_start = ref_html.index('<style>') + 7
css_end = ref_html.index('</style>')
css = ref_html[css_start:css_end].strip()

html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>这场顶级饭局，细节全在座位里</title>
<style>
{css}
</style>
</head>
<body>
<div class="aw">
<div class="cover">
<div class="ct">
<div class="ct-tag">深度解读</div>
<div class="ct-title">这场顶级饭局<br>细节全在座位里</div>
<div class="ct-sub">从国宴合影看社交密码与权力秩序</div>
</div>
</div>
<div class="c">

<div class="lead">
国宴的照片和视频陆续流出，里面有几个细节值得一聊。从雷军找马斯克合影引发全网争议，到座次安排里藏着的权力秩序——这场顶级饭局的每一个细节，都在告诉我们一些不一样的东西。
</div>

<!-- 1 -->
<div class="st"><span class="sn">1</span><span class="stx">雷军找马斯克合影：蹭热度还是社交智慧？</span></div>

<p>先从最热的话题开始——雷军找马斯克合影。这件事在网上吵得很厉害，很多人的反应是：雷军好歹也是大佬，小米创始人，身家200多亿美元，怎么能像个小迷弟一样去求合影？</p>

<p>然后大家开始分析现场视频，越分析越起劲。有人说你看雷军的姿势，身体是微微蹲着的，像是在迁就马斯克的坐姿，显得很低姿态。再看马斯克那边，屁股压根没抬，手势也没有，就对着镜头挤了个眼，表情还有点僵，整个人感觉有点敷衍。</p>

<p>于是网上就开始有声音说，雷军真是被流量所累，为了蹭热度面子都不要了。还有人上升到社交方式的高度，说雷军这种直接找马斯克要合影的行为是一种"无效社交"——只有形式上的同框，没有价值交换，没有情感联结，没有任何后续价值，纯粹是单向索取。</p>

<div class="wc">
<h4>🤔 两种声音</h4>
<ul>
<li><b>批评派</b>：姿态太低，丢了中国企业家的面子，属于无效社交</li>
<li><b>理解派</b>：雷军本来就是营销高手，这个合影带来的流量和话题度，远超任何广告投放</li>
</ul>
</div>

<!-- 2 -->
<div class="st"><span class="sn">2</span><span class="stx">无效社交？你可能误解了雷军</span></div>

<p>但说这是"无效社交"，可能把事情想简单了。</p>

<p>首先，雷军不需要通过一张合影来证明什么。他完全可以在自己的主场——中国科技圈——呼风唤雨。但他选择走出去，主动跟全球科技领袖建立联系，这本身就是一种战略性的社交布局。</p>

<p>其次，合影只是一个起点。在国际场合的每一次露面、每一次握手、每一次同框，都是在为后续更深层的合作铺路。谁说合影之后不会有邮件、不会有会议、不会有商业合作？</p>

<p>再者，雷军的"低姿态"可能恰恰是一种高情商的表现。在别人的主场，适当放低姿态不是示弱，而是尊重。真正的大佬，不需要处处彰显自己的地位。</p>

<p>有意思的是，马斯克虽然表情看起来敷衍，但他答应了合影。这说明他至少不排斥这个互动。在顶级社交场合，一个愿意的合影，本身就是一个信号。</p>

<!-- 3 -->
<div class="st"><span class="sn">3</span><span class="stx">国宴座次：一张座位表里的权力密码</span></div>

<p>比合影更有看头的是国宴的座次安排。在正式的外交场合，座次从来不是随便安排的，每一个位置都有讲究。</p>

<div class="ic">
<h4>🪑 座次规则解读</h4>
<ul>
<li><b>主桌核心位置</b>：距离主宾最近的座位，代表最高的外交礼遇</li>
<li><b>左右之分</b>：在某些文化中，右侧地位高于左侧；在某些场合则相反</li>
<li><b>对面位置</b>：能直接与主宾对视交谈的位置，通常安排重要人物</li>
<li><b>远近之分</b>：距离主桌越近，代表关系越密切或地位越重要</li>
</ul>
</div>

<p>从流出的照片看，科技企业家的座次安排本身就透露了大量信息——谁被安排在了更核心的位置，谁被安排在了相对边缘的位置，这些细节都在无声地传递信号。</p>

<!-- 4 -->
<div class="st"><span class="sn">4</span><span class="stx">饭局社交的底层逻辑</span></div>

<p>国宴这种级别的饭局，吃饭从来不是重点。重点是人在什么位置，跟谁坐在一起，说了什么话。</p>

<p>在中国的社交文化里，饭局是最重要的社交场景之一。座次安排、谁先动筷、谁先敬酒、谁最后离场——每一个细节都是信号。</p>

<p>而在国际场合，这些信号更加复杂，因为还叠加了文化差异和外交礼仪。一个看似简单的座次，背后可能是数轮外交磋商的结果。</p>

<div class="wc">
<h4>🍽️ 顶级饭局的关键看点</h4>
<ul>
<li><b>谁来了</b>：受邀本身就是信号——代表你在某个领域的重要性</li>
<li><b>坐在哪</b>：座次代表关系亲疏和地位排序</li>
<li><b>跟谁聊</b>：席间的交流往往比正式会议更有效</li>
<li><b>怎么聊</b>：敬酒、寒暄、交换联系方式——每一步都有讲究</li>
</ul>
</div>

<!-- 5 -->
<div class="st"><span class="sn">5</span><span class="stx">企业家的"破圈"社交</span></div>

<p>雷军这次的合影事件，其实折射出一个更大的趋势：中国企业家正在积极"破圈"，主动融入全球商业社交网络。</p>

<p>过去，很多中国企业家习惯于在自己的一亩三分地里当"土皇帝"，对国际社交不够重视。但如今，随着中国企业的全球化，企业家们也越来越意识到——人脉就是资源，社交就是生产力。</p>

<p>从这个角度看，雷军主动找马斯克合影，不是"低三下四"，而是一种战略性的社交投资。一次合影的价值，不在于当下能换回什么，而在于它为未来的可能性打开了一扇门。</p>

<p>当然，也有人担心这种"合影社交"会流于表面。毕竟真正的商业合作，靠的是实力和诚意，而不是一张照片。但至少，它是一个起点。</p>

<!-- 6 -->
<div class="st"><span class="sn">6</span><span class="stx">社交的三个层次</span></div>

<p>从这次国宴的讨论中，我们可以提炼出社交的三个层次：</p>

<div class="sg">
<div class="sb sp">
<h5>🔹 第一层：形式社交</h5>
<p>合影、寒暄、交换名片<br>价值：建立初步印象<br>风险：流于表面</p>
</div>
<div class="sb sr">
<h5>🔹 第二层：价值社交</h5>
<p>资源交换、互利合作<br>价值：创造实际收益<br>关键：等价交换</p>
</div>
</div>

<div class="sg">
<div class="sb sp">
<h5>🔹 第三层：关系社交</h5>
<p>深度信任、长期伙伴<br>价值：超越利益的连接<br>核心：真诚和时间</p>
</div>
<div class="sb sr">
<h5>💡 关键认知</h5>
<p>三个层次不是割裂的<br>第一层是第二层的入口<br>第二层是第三层的基础<br>没有起点就没有后续</p>
</div>
</div>

<!-- 7 -->
<div class="st"><span class="sn">7</span><span class="stx">结语：别急着嘲笑主动社交的人</span></div>

<p>很多人嘲笑雷军的合影行为，觉得他"掉价"。但如果换个角度想，敢于主动社交、敢于放低姿态的人，往往比那些端着架子的人走得更远。</p>

<p>真正的自信，不是在所有场合都要表现得高高在上，而是该高的时候能高，该低的时候能低。雷军能放下身段去求合影，恰恰说明他心里有更大的格局。</p>

<p>而那些嘲笑他的人，可能连走进那个饭局的资格都没有。</p>

<div class="dv"></div>

<div class="sc">
<h4>📌 本文要点</h4>
<ul>
<li>雷军与马斯克合影引发争议，但"无效社交"的说法可能过于简单</li>
<li>国宴座次安排暗藏权力密码，每个位置都有讲究</li>
<li>社交分三个层次：形式→价值→关系，层层递进</li>
<li>主动社交是一种战略投资，不是"掉价"</li>
<li>真正的自信是能高能低，而不是永远端着</li>
</ul>
</div>

<div class="dv"></div>

<div class="ft">
<span>深度解读</span>
<span>社交密码</span>
<span>国宴</span>
<span>企业家</span>
</div>

</div>
</div>
</body>
</html>'''

with open(tmp_file, 'w', encoding='utf-8') as f:
    f.write(html)

print(f'Temp file: {tmp_file}')
print(f'Size: {len(html)} chars, {len(html.encode("utf-8"))} UTF-8 bytes')
