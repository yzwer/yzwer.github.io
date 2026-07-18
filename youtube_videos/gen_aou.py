# -*- coding: utf-8 -*-
"""Generate WeChat article for aOuFC_wWJo8"""
import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')

base = r'C:\Users\11132\.qclaw\workspace-yw3plsutb1jupnif\youtube_videos'
vid = 'aOuFC_wWJo8'
tmp_file = os.path.join(os.environ.get('TEMP','/tmp'), '_tw_aou.html')

# Read CSS from reference article
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
<title>几个留学生犯案，轰动了整个欧洲：中国版"恩浩房"事件全记录</title>
<style>
{css}
</style>
</head>
<body>
<div class="aw">
<div class="cover">
<div class="ct">
<div class="ct-tag">深度调查</div>
<div class="ct-title">几个留学生犯案<br>轰动了整个欧洲</div>
<div class="ct-sub">中国版"恩浩房"事件——德国中国留学生迷奸案完整记录</div>
</div>
</div>
<div class="c">

<div class="lead">
最近在德国乃至整个欧洲，有一个案子非常轰动，但国内居然没怎么报道——一群中国留学生合伙在国外迷奸同胞，被称为"中国版恩浩房事件"。一个核心群组8人协作分工，长期交流如何对华人女性实施迷奸及拍摄暴力色情影像，下游聊天群组成员规模达约4500人，运营长达4年。
</div>

<!-- 1 -->
<div class="st"><span class="sn">1</span><span class="stx">"德国老司机"群组：系统性迷奸网络</span></div>

<p>在一个名为"德国老司机"群聊的核心群组里，8个核心成员协作分工，长期交流如何对华人女性实施迷奸及拍摄暴力色情影像。</p>

<p>他们的讨论内容包括：</p>

<div class="wc">
<h4>🔴 群组内的讨论内容</h4>
<ul>
<li>如何给女性下药并强奸她们</li>
<li>使用什么药物、剂量多少</li>
<li>在女性失去意识后对他们做什么</li>
<li>强奸时使用什么物品和工具</li>
<li>拍摄受害者的照片和视频，在群组下游聊天群里分享</li>
</ul>
</div>

<p>其中最大一个相关群组成员规模达约4500人，而长期活跃参与讨论下药经验及分享偷拍影像的群组成员超过2000人，运营长达4年。</p>

<p>在这些聊天记录里，他们自称"司机"，把目标女性叫做"汽车"，其中熟人或朋友介绍来的目标被称为"二手车"。</p>

<!-- 2 -->
<div class="st"><span class="sn">2</span><span class="stx">案件曝光：一次偶然的发现</span></div>

<p>案件的曝光源于一位受害者的勇敢举报。受害女性在发现自己的私密影像被传播后，选择向德国警方报案。警方介入调查后，顺藤摸瓜逐步揭开了这个庞大的犯罪网络。</p>

<p>调查显示，犯罪嫌疑人的作案模式高度相似：通过社交场合结识华人女性，在饮品中下药，待受害者失去意识后实施性侵，并全程拍摄。这些影像随后被上传至多个聊天群组供人"观赏"和"交流经验"。</p>

<p>更令人震惊的是，群组中的部分成员不仅是旁观者，还会根据他人分享的"经验"来改进自己的作案手法——这已经形成了一个完整的犯罪学习和传播链条。</p>

<!-- 3 -->
<div class="st"><span class="sn">3</span><span class="stx">嫌疑人身份：高学历留学生</span></div>

<p>令整个华人社区震惊的是，被捕的嫌疑人大多是正在德国就读的中国留学生，其中不乏名校学生。他们拥有良好的教育背景、体面的外表，却在暗处从事如此恶劣的犯罪行为。</p>

<p>这种反差让很多人难以接受——那些在课堂上认真听讲、在图书馆埋头苦读的年轻人，转身却成了精心策划犯罪的加害者。</p>

<p>案件曝光后，德国华人社区一片哗然。许多在德中国留学生和华人表示，这不仅是对受害者的伤害，更是对整个华人群体声誉的严重损害。</p>

<!-- 4 -->
<div class="st"><span class="sn">4</span><span class="stx">法律追踪：德国司法如何处理</span></div>

<p>德国法律对于性侵犯罪有严格的规定，尤其是涉及下药、团伙作案和影像传播等加重情节，刑罚将更为严厉。</p>

<div class="ic">
<h4>⚖️ 德国相关法律</h4>
<ul>
<li><b>性侵罪（Sexuelle Nötigung/Vergewaltigung）</b>：根据德国刑法第177条，使用药物使被害人失去抵抗能力后实施的性行为，属于严重性侵，可处3年以上15年以下有期徒刑</li>
<li><b>团伙犯罪加重</b>：多人协作实施性侵属于加重情节，刑期上限可进一步提高</li>
<li><b>影像传播</b>：未经同意拍摄和传播私密影像，违反德国刑法第184条，可并处罚金和有期徒刑</li>
<li><b>下药犯罪</b>：故意在他人饮品中投放药物，本身就构成独立犯罪</li>
</ul>
</div>

<p>值得注意的是，德国没有死刑，最高刑罚为终身监禁。但对于如此恶劣的团伙犯罪，涉案人员很可能面临长期甚至接近最高刑期的判决。</p>

<!-- 5 -->
<div class="st"><span class="sn">5</span><span class="stx">受害者的困境</span></div>

<p>在这类案件中，受害者往往面临多重困境：</p>

<div class="wc">
<h4>💔 受害者面临的问题</h4>
<ul>
<li><b>羞耻感和自我责备</b>：许多受害者在事发后不敢声张，甚至不确定自己是否遭到了性侵</li>
<li><b>影像传播的二次伤害</b>：私密影像被数千人观看和传播，造成的心理创伤难以估量</li>
<li><b>异国他乡的无助</b>：身处国外，语言障碍、对当地法律不了解，增加了求助的难度</li>
<li><b>社群压力</b>：华人社区规模有限，担心声张后遭受非议和孤立</li>
<li><b>法律程序漫长</b>：德国司法程序通常较为缓慢，受害者需要反复面对证词和质证</li>
</ul>
</div>

<p>然而，正是这些受害者的勇气——选择站出来报案、配合调查、出庭作证——才让这个隐藏4年的犯罪网络最终被揭露。</p>

<!-- 6 -->
<div class="st"><span class="sn">6</span><span class="stx">留学生社区的反应</span></div>

<p>案件曝光后，在德中国留学生社区的反应是复杂的。愤怒、震惊、羞耻、担忧交织在一起。</p>

<p>许多留学生自发组织起来，发布安全提醒、分享防范知识。有人在社交媒体上呼吁："出门不要让饮品离开视线，不要接受陌生人递来的饮料，即使是在熟人聚会上也要保持警惕。"</p>

<p>也有人反思：为什么这样的犯罪能在留学生群体中持续4年而未被及时发现？是文化中的沉默习惯，还是对"自己人"的过度信任？</p>

<p>一位在德多年的华人在社交媒体上写道："这件事让我明白，坏人不会把'坏人'写在脸上。学历、背景、外表都不能代表一个人的品行。保护好自己，永远不要放松警惕。"</p>

<!-- 7 -->
<div class="st"><span class="sn">7</span><span class="stx">反思：如何防止悲剧重演</span></div>

<p>这起案件带来的教训是深刻而沉痛的。它不仅是一起刑事案件，更暴露了留学生群体在安全意识、社区互助和法律保护方面的多重短板。</p>

<div class="sg">
<div class="sb sp">
<h5>🛡️ 个人防范</h5>
<p>聚会不让饮品离视线<br>不接陌生人递的饮料<br>与信任的朋友同行<br>察觉异常立即求助<br>发现被侵犯勇敢报警</p>
</div>
<div class="sb sr">
<h5>🌐 社区层面</h5>
<p>建立安全互助网络<br>畅通的举报渠道<br>消除受害者羞耻文化<br>对性侵零容忍态度<br>定期开展安全宣导</p>
</div>
</div>

<p>更重要的是，我们需要打破沉默的文化。当有人遭遇侵害时，不应该是受害者感到羞耻，而应该是加害者付出代价。每一个选择沉默的旁观者，客观上都为犯罪的延续提供了土壤。</p>

<div class="dv"></div>

<div class="sc">
<h4>📌 案件要点</h4>
<ul>
<li>核心群组8人协作，运营迷奸犯罪网络长达4年</li>
<li>下游群组达4500人规模，活跃参与者超2000人</li>
<li>嫌疑人多为在德中国留学生，不乏名校背景</li>
<li>德国法律对此类犯罪处罚严厉，最高可判终身监禁</li>
<li>受害者的勇气是案件得以揭露的关键</li>
</ul>
</div>

<div class="dv"></div>

<div class="ft">
<span>深度调查</span>
<span>留学生安全</span>
<span>德国</span>
<span>迷奸案</span>
</div>

</div>
</div>
</body>
</html>'''

with open(tmp_file, 'w', encoding='utf-8') as f:
    f.write(html)

print(f'Temp file: {tmp_file}')
print(f'Size: {len(html)} chars, {len(html.encode("utf-8"))} UTF-8 bytes')
