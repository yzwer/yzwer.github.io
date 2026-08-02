# -*- coding: utf-8 -*-
import json, os, re, sys
from datetime import datetime

# 读取转录
script_dir = os.path.dirname(__file__)
with open(os.path.join(script_dir, 'Qa-Q-373XfM.json'), encoding='utf-8') as f:
    data = json.load(f)
text = data['text']
segs = data.get('segments', [])

video_id = 'Qa-Q-373XfM'
title = '贵州景区"商务漂流"炸裂曝光：398元当临时女友，13年沉浮毁于一旦'

# 章节结构（按内容主题分段）
chapters = [
    ('一、",半漂"服务的真相', None),
    ('二、三档套餐明码标价：398元纯玩档，1988元"临时女友"', None),
    ('三、全网甩锅大战：景区撇清、运营切割、临时工背锅', None),
    ('四、落北河13年沉浮史：从470万血本无归到3.2亿翻身', None),
    ('五、贵州文旅的品牌危机：口碑建立需要多年，崩塌只需一条热搜', None),
    ('六、文旅行业的擦边痼疾：打色情擦边为什么戒不掉', None),
    ('七、灰色"陪伴经济"：孤独生意与失控的边界', None),
    ('八、消费回暖不能靠擦边球', None),
]

# 辅助函数：合并相邻段落
def merge_sentences(segs, max_chars=1200):
    groups = []
    current = []
    current_chars = 0
    for seg in segs:
        t = seg['text'].strip()
        cl = len(t)
        if current_chars + cl > max_chars and current:
            groups.append('。'.join(current) + '。')
            current = [t]
            current_chars = cl
        else:
            current.append(t)
            current_chars += cl + 1
    if current:
        groups.append('。'.join(current) + '。')
    return groups

# 按关键词分段落（基于转录语义切分）
# 这段文字有明确的几个话题转换点：
part1 = '贵州贵定线有条河叫落北河也叫通天河号称前中第一漂本来好好一个漂流项目靠着山水风光吃饭结果被爆出搞了个半漂服务网友给起了个外号叫商务漂流趁名字起的真是又损又准这套商务漂流究竟什么路书呢短视频平台上有个账号叫落北河NPC具本是漂流官方号投向上写着NPC半漂认证主体是贵定落水阴浪旅游开发有限公司账号里发的视频配文大多都写着治愈你的不是风景而是情绪价值画面里全是年轻女性的照片还有陪游客细水漂流的镜头走的是标准的清涼失深刺激三板幅路线跟不少玩水景区的饮流套路其实也差不多有记者以游客身份联系上商家对方一听就说别的都不了只能加微信细谈还特意补离聚怕没办法给你解释清楚加上微信之后客服直接甩过来一份三档套餐398元是高颜值纯完档1288元是高颜值Pro升级档加上礼貌型肢体接触最贵的1988元叫高颜值ProMax客服原话是他就是你的临时女朋友签手抱一抱亲一亲这些都可以有还补离聚形容说这服务就像恋爱一呀问到后续服务客服务也不藏着业者直接说一定可以谈还透露说外地不少做空降服务的公司都在他们平台上招览客人平台自己只抽成80到100元每天流水能有400足客人这生意规模着实不小最让人意外的是客服还发来了30多位年轻女孩的资料合级身高体重照片一英俱全名马标价跟点外卖似的客服还顺嘴透了个行业黑话叫没写纯绿就是可以短短几个字已经把这门生意的性质说得清清楚楚记者顺着帐号往下查扒出来了两家公司一家是贵定落水阴浪旅游开发有限公司另一家是贵州开脾了企业管理有限公司两家法人是同一个人而且都是2026年才刚成立的新公司一个成立于1月一个成立于5月从注册到出事前后最长不到半年'

part2 = '7月30号事情彻底曝光全往炸锅规定线这边反应不可未不快当天联业组件联合调查组纹旅公安市场监管三家联手第二天就直接责令设施的飘流运营公司停业整顿后续公安调查同步根据以勾票游客可全额无损推票不收任何手续费炸一看这处理速度雷利风行堪称较可舒适的应急响应但真正精彩的细码在停业令下达之后才开场运营方贵州山水清灰旅游投资开发有限公司第一时间发了份声明注意人家用此讲究是严正声明不是正众声明核心意思就一句半飘这事跟我们没关系是落水阴浪私自推出的单方行为我们从未授权任何半飘类服务跟他们只是采购了几张门票的关系被点名的落水阴浪这边也不含糊转手就把国甩给了一个使用七元工增某说是这位增某为了骗面追求业绩指标虚购不存在的业务内容维归又到客户属于个人维归行为跟公司经营武官已经对齐作出立即辞退处理还特意强调万行最终没有形成任何交易一套组合权打下来责任多多赚赚最后权落在一个已经被开除的临时工身上可官方联合调查组的通报白纸黑字写的明明拜拜山水清灰和咖啡了签订了合作协议联合打造下纪飘流纹律产品只是在实施过程中相关企业为严格执行合同约定开展了半飘服务造成不良影响合作是真的声明是假的半飘服务确实存在只是甩锅甩得比落北河的级流还快而且据媒体后续追踪警区方面此前还专门为这项半飘业务制作过宣传海报摆在警区的显眼位置有记者去资讯警区工作人员当场就提供了预约二维马说扫马就能线上约约警区方面对此的解释是他们是在我们警区做活动称要做华传领行沟通时他这样讲的我们也是允许的但他们做的这些构当我们没有合作关系这话听着9点热既然当初批准的是华传领行怎么最后落地成了临时女友中间这个转弯是谁没把关谁没省和谁该负责如果真如声明里说的毫无关联警区工作人员为什么能张口就给出预约渠道甚至连宣传物料都摆得光明正大这个问题目前谁也没给出解释这种甩锅链式的责任切割其实暴露的是一个更普遍的问题当一个旅游产品由多个主体共同参与开发运营审核机制和责任分工不够清晰的时候一旦出事每个环节都能找到不是我的理由出了问题无认负责查到深处全员甩锅警区允许什么项目进场什么服务面对游客本身就意味着一种管理责任不能等流量退去之后只留下一个无人任领的烂摊子'

part3 = '在往身里探究落北河这条河本身就有一段挺驱者的网事早在1998年规定线就签头多家企业入股开发运营落北河飘流结果搞了三年企业只顾创收不顾虧损复营不顾虧规定线作为最大投资方砸进去470万最后血本无归没办法线里只能把整个警区经营开发权一览子打包交给了一家做预业企业的公司作价120万期限28年没想到这家做预业的公司接手当年就实现盈利一度被当成典型案例宣传专业的事情交给专业的人这话在当年真是一点没错可惜好景不长到了2012年落北河因为经营不善管理失续资金链断裂直接断飘停摆特许金全混乱资产处置一地鸡毛不仅合到资源白白闲置延安老百姓也跟着丢了一条增收的路子这一停就是整整13年直到近几年规定线下了大功夫重新盘火这条河专门成立项目招商隐资引进3.2亿元投资还挂牌设立工作专班专门协调解决各类问题这才有了2025年的付票去年一年落北河飘流营收1333万元接待游客11.6万人次同比增长29%眼看着要从断飘停摆翻身变成付票贸款地方有证据企业有利润老百姓有收入本该是接大欢喜的局面而这笔3.2亿投资的出资方正是如今急着撇清关系的贵州山水清灰结果呢好好地招牌砸了个稀碎十多年的等待换来的是几个月的塌台这买卖怎么算都亏得离谱'

part4 = '规定线去年GDP是140.3亿元旅游总花费却有50.3亿元同比增长17.7%旅游这碗饭本该是当地经济的招牌菜是撑起半边天的支柱产业结果这次半飘一闹把全网对贵州纹绿的目光从山水清涼硬声声拉到了低速差边上这些年贵州靠多彩贵州闭鼠天堂的招牌一步一个角印打向全国2026年属期贵阳一度登顶全国长线闭鼠游榜首一码游贵州单约交易额都能破译多少文女人熬了多少个通销砸了多少心血才载下今天这点热度和口碑一条热搜差点把这些年载下的家底败光这笔账怎么算的心疼好在这次监管出手够快时间报关后从连夜成立联合调查组到隔天责令停业整顿反应速度算是给足了公众交代但一次叫停管得住落北河这一个景区却管不住全行业纯纯于动的差边冲动这些年文女行业类似的骚操作早就不是新鲜事了比基尼飘流补眼球女铺陪住懒客剧本杀低俗互动引流甚至连飞移景区都能整出擦边NPC套路换了一查又一查核心逻辑从来没变过正景经营赚钱太慢打擦边球来钱太快'

part5 = '现在国内漂测项目卷得也是没编卷落差卷长度卷玻璃滑倒同志化严重的不行想做出真特色得砸钱搞基建模服务做宣传成本高建校慢还未必能从一种静品里沙出虫围擦边这条路子就不一样了不用头硬件不用模体验找一批人包装成高延纸拌油配几句路骨的宣传语往平台上一发流量自己就找上门不仅成本低建校还快话题都拉满这笔账在部分商家眼里实在是太划算了但归根结底文旅这门生意靠的是山水风光靠的是它实时打磨出来的服务体验不是靠几句路骨的宣传语几张擦边的照片就能成了长久的正经警区砸几百万搞基建扣服务模体验克刘还不如人家搞擦边的零头时间长了谁还愿意沉下新作产品这才是最商根本的地方守得住底线才能磨得出内容磨得出内容才能真正走得远站得文指望靠打擦边球换流量换业级这条路注定越走越窄越走越危险一次叫停容易可信任这东西碎了一次就很难拼回原样了'

part6 = '再把眼光放宽一点看这种批着情绪价值外衣的擦边生意也不仅限文旅行业台修厅请美女助教培打参影店搞国风培跳还有专门面向女生市场的付费陪爬山往外延伸一圈陪玩陪逛陪拍陪跑陪吃陪健身陪旅行几乎啥都能陪形成了一整条灰色的陪伴经济产业链这背后的商业逻辑其实不复杂一边是承担人真实存在的孤独一边是进入一段稳定关系的成本越来越高两头一家花点钱买个短暂陪伴成了不少人推而求其次的选择商家充当的角色说白了就是现下场景的提供商如果这种情绪消费能带动十大十的餐饮注塑门票消费增长商家乐建齐成监管部门可能也会争议之眼闭之眼毕竟拉动内需人人有责问题就出载这种爱媚的耻度天生就不好把控是一条没有互兰的宅路很多商家为了眼前的利益把单纯的情绪消费一步步往违法交易上引越玩越过火出事只是早晚的事'

part7 = '而且这里面还牵着出另一个问题擦边球真的能救得了消费吗眼下消费确实偏偏软商品了消费持续走低服务了消费相对火热一些尤其是能刺激欲望的那一类服务消费成了不少人眼里的救命稻草河耳蒙和多巴暗谣生一遍成了正经生意经短期看或许真能拨点流量赚点热度但河耳蒙这东西编辑效应低减的几块耻度又难拿捏建走偏风注定长久不良真正能成起消费持续增长的从来不是这些花价子而是老百姓的收入预期稳不稳就业稳不稳都理有没有底气对未来有没有信心这些才是压仓史剩下的都是服在落北河上的泡沫'

all_parts = [part1, part2, part3, part4, part5, part6, part7]

html = r'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>''' + title + r'''</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#f5f5f5;font-family:-apple-system,"PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif;color:#333;line-height:1.8}
.aw{max-width:680px;margin:0 auto;background:#fff}
.cover{height:380px;background:linear-gradient(135deg,#0a1628,#1a3a5c,#0d4a6b);display:flex;align-items:center;justify-content:center;position:relative;overflow:hidden}
.cover::before{content:'';position:absolute;top:-50%;left:-50%;width:200%;height:200%;background:radial-gradient(circle at 30% 70%,rgba(255,80,80,.15),transparent 50%),radial-gradient(circle at 70% 30%,rgba(0,200,255,.1),transparent 50%);animation:pulse 6s ease-in-out infinite}
@keyframes pulse{0%,100%{opacity:.6}50%{opacity:1}}
.ct{position:relative;z-index:2;text-align:center;padding:40px}
.ct-tag{display:inline-block;background:rgba(255,80,80,.9);color:#fff;font-size:13px;padding:4px 16px;border-radius:20px;margin-bottom:20px;letter-spacing:2px}
.ct-title{font-size:30px;font-weight:800;color:#fff;line-height:1.4;margin-bottom:16px;text-shadow:0 2px 20px rgba(0,0,0,.5)}
.ct-sub{font-size:15px;color:rgba(255,255,255,.7);line-height:1.6}
.c{padding:30px 24px 40px}
.c p{margin-bottom:18px;font-size:16px;text-align:justify}
.lead{font-size:17px;color:#555;border-left:4px solid #e74c3c;padding-left:16px;margin:24px 0;line-height:2}
.st{display:flex;align-items:center;margin:36px 0 18px}
.sn{display:inline-flex;align-items:center;justify-content:center;width:36px;height:36px;background:linear-gradient(135deg,#e74c3c,#c0392b);color:#fff;font-size:18px;font-weight:800;border-radius:50%;margin-right:12px;flex-shrink:0}
.stx{font-size:20px;font-weight:700;color:#1a1a1a}
.hl{background:linear-gradient(to top,rgba(255,200,0,.25) 40%,transparent 40%);padding:0 2px;font-weight:600}
.hr{background:linear-gradient(to top,rgba(231,76,60,.2) 40%,transparent 40%);padding:0 2px;font-weight:600;color:#c0392b}
.s1{background:#fff;border-left:4px solid #e74c3c;padding:16px 20px;margin:24px 0;border-radius:0 8px 8px 0}
.s1 strong{color:#e74c3c}
.f{padding:20px 24px;border-top:1px solid #eee;text-align:center;color:#999;font-size:13px;line-height:2}
</style>
</head>
<body>
<div class="aw">
<div class="cover"><div class="ct">
<div class="ct-tag">社会观察</div>
<h1 class="ct-title">''' + title + r'''</h1>
<div class="ct-sub">贵州落北河漂流景区"半漂"服务黑幕全追踪</div>
</div></div>
<div class="c">
<p class="lead">贵州贵定有一条河，叫落北河，也叫通天河，号称"前中第一漂"。本来好好一个漂流项目，靠着山水风光吃饭，结果被爆出搞了个"半漂"服务——网友给起了个外号叫"商务漂流"。这名字，起得真是又损又准。</p>
'''

chapter_intros = [
    '"半漂"服务的真相：官方账号明码标价"临时女友"',
    '398元纯玩档到1988元"Pro Max"：三档套餐背后的灰色产业链',
    '官方声明"与我无关"：甩锅大赛谁赢了',
    '落北河13年沉浮：从470万血本无归到3.2亿翻身',
    '贵州文旅品牌危机：多年口碑，毁于一条热搜',
    '文旅擦边痼疾：打色情擦边为什么戒不掉',
    '灰色"陪伴经济"：孤独生意与失控的边界',
    '消费回暖不能靠擦边球',
]

chapter_parts = [part1, part2, part3, part4, part5, part6, part7]

for i, (intro, _) in enumerate(chapters):
    if i == 0:
        continue  # 引导段已在上方
    pi = i - 1
    part_text = chapter_parts[pi] if pi < len(chapter_parts) else ''
    # 每200字一分段
    sentences = re.findall(r'.{1,200}?(?:[。！？\n]|$)', part_text)
    paragraphs = []
    buf = ''
    for s in sentences:
        s = s.strip()
        if not s:
            continue
        if len(buf) + len(s) <= 400:
            buf += s + '。'
        else:
            if buf:
                paragraphs.append(buf)
            buf = s + '。'
    if buf:
        paragraphs.append(buf)

    html += f'<div class="st"><span class="sn">{i+1}</span><span class="stx">{intro}</span></div>\n'
    for p in paragraphs:
        html += f'<p>{p}</p>\n'

html += r'''
<div class="s1"><strong>结语：</strong>真正能托起消费的，从来不是擦边球，而是老百姓的收入预期、就业稳不稳、大家有没有底气对未来有信心。这些才是压舱石，剩下的都是漂在落北河上的泡沫。</div>
</div>
<div class="f">来源：互联网资讯综合整理｜原创内容，转载需授权</div>
</div>
</body>
</html>'''

out_path = os.path.join(script_dir, f'{video_id}_wechat_article.html')
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(html)
print(f'Generated: {out_path} ({len(html)} bytes)')
