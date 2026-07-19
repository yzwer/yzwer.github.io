---
title: "AI时代的雷曼兄弟？深度拆解OpenAI泡沫论"
date: 2026-07-18T19:14:24+08:00
draft: false
description: "知名科技空头Ed Zitron万字长文：OpenAI商业模式有根本性缺陷，一旦倒下将引发AI产业链连锁崩塌——堪比2008年金融危机的\"雷曼时刻\"正在AI行业酝酿？"
---

{< inline_style >}
* { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "PingFang SC", "Microsoft YaHei", sans-serif; line-height: 1.8; color: #333; background-color: #f5f7fa; padding: 20px; }
        .container { max-width: 680px; margin: 0 auto; background: #fff; border-radius: 8px; box-shadow: 0 2px 12px rgba(0,0,0,0.08); overflow: hidden; }
        .header { background: linear-gradient(135deg, #1b1b1b 0%, #3c0000 50%, #5c1010 100%); color: #fff; padding: 40px 30px; text-align: center; }
        .header h1 { font-size: 26px; font-weight: 600; margin-bottom: 12px; line-height: 1.4; }
        .header .subtitle { font-size: 14px; opacity: 0.85; }
        .content { padding: 30px; }
        h2 { font-size: 20px; color: #3c0000; margin: 30px 0 18px; padding-bottom: 10px; border-bottom: 2px solid #f5e0e0; font-weight: 600; }
        h2:first-child { margin-top: 0; }
        p { font-size: 16px; margin-bottom: 16px; text-align: justify; }
        .highlight-box { background: #fff8e1; border-left: 4px solid #f9a825; padding: 18px 20px; margin: 24px 0; border-radius: 0 6px 6px 0; }
        .highlight-box p { margin: 0; color: #5d4e00; font-weight: 500; }
        .highlight-red { background: #ffebee; border-left: 4px solid #c62828; padding: 18px 20px; margin: 24px 0; border-radius: 0 6px 6px 0; }
        .highlight-red p { margin: 0; color: #b71c1c; font-weight: 500; }
        .highlight-green { background: #e8f5e9; border-left: 4px solid #2e7d32; padding: 18px 20px; margin: 24px 0; border-radius: 0 6px 6px 0; }
        .highlight-green p { margin: 0; color: #1b5e20; font-weight: 500; }
        .data-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; margin: 20px 0; }
        .data-card { background: #f0f4f8; padding: 15px; border-radius: 6px; text-align: center; }
        .data-card .number { font-size: 20px; font-weight: 700; color: #c62828; }
        .data-card .label { font-size: 13px; color: #666; margin-top: 4px; }
        strong { color: #5c1010; }
        .quote-box { background: #f5f5f5; border-left: 4px solid #5c1010; padding: 16px 20px; margin: 20px 0; border-radius: 0 6px 6px 0; font-style: italic; }
        .quote-box p { margin: 0; color: #444; }
        .footer { background: #f8f9fa; padding: 20px 30px; text-align: center; font-size: 13px; color: #888; border-top: 1px solid #eee; }
        @media (max-width: 480px) {
            .header { padding: 30px 20px; }
            .header h1 { font-size: 22px; }
            .content { padding: 20px; }
            h2 { font-size: 18px; }
            .data-grid { grid-template-columns: 1fr; }
        }
{< /inline_style >}

<h2>一、万字长文引爆AI业：OpenAI＝AI时代的雷曼兄弟？</h2>
<p>最近一篇万字长文，把本就风声鹤唳的AI行业搅得更加人心惶惶。写这篇文章的人叫埃德·奇特隆（Ed Zitron），是科技圈里出了名的AI唱空派，粉丝众多、观点一向激进。这次它抛出了迄今为止最狠的一个判断——<strong>所谓的AI泡沫，根本不是什么行业性泡沫，而是彻头彻尾的OpenAI泡沫</strong>。</p>
<p>它甚至放话：OpenAI的商业模式有根本性缺陷。如果OpenAI最终倒下，它将成为AI时代的雷曼兄弟——不光自己完蛋，还会把整个数据中心产业、AI基础设施、乃至全球科技股的估值体系一起拖下水。</p>
<p>这篇文章发布之后很快被大量金融媒体转载讨论。媒体总结奇特隆的核心观点是：问题不在于AI这项技术到底有没有价值，而在于OpenAI这家公司究竟有没有一套能够撑起整个AI资本周期的商业模式。如果答案是否定的，那么围绕OpenAI搭建起来的融资体系、算力投资体系和资本开支体系，都可能面临连锁式的崩塌。</p>

<div class="quote-box">
<p>"OpenAI早就不只是一家公司了，它更像是整个AI投资周期里的那个系统性重要机构。一旦这块基石松动，冲击面会远远超出它自己。"</p>
</div>

<h2>二、商业模式的三重缺陷</h2>
<p>奇特隆凭什么说OpenAI的商业模式有根本性缺陷？它列了三条理由：</p>
<p><strong>第一，推理成本压不下来</strong>。用户规模越大，每一次提问背后的GPU开销、电费、服务器成本就跟着涨。如果大量用户长期停留在低价甚至免费套餐上，企业级收入又跟不上覆盖这些成本，那规模扩张带来的就不是利润扩张，而是亏损扩张。</p>
<p><strong>第二，资本开支远超现金流改善</strong>。现在AI行业花钱最多的地方已经不再是训练模型，而是推理算力——GPU采购和全球数据中心建设。OpenAI和它的合作伙伴正在推动数百亿甚至更大规模的IDC项目，这些项目往往要好几年才能回本。一旦未来AI需求增长不及预期，大批基础设施就会面临利用率不足。</p>
<p><strong>第三，持续依赖外部融资</strong>。奇特隆判断OpenAI在未来很多年里都需要不停融资来覆盖研发、算力采购和基建开销。一旦资本市场风险偏好下降或融资环境收紧，它的商业模式就会承受更大压力。</p>

<div class="highlight-red">
<p>用户越多亏得越多、资本开支远超现金流、永远在找下一轮融资——OpenAI的"增长飞轮"可能只是"烧钱循环"的包装。</p>
</div>

<h2>三、比OpenAI更危险的是整条产业链的杠杆</h2>
<p>比起OpenAI本身，奇特隆更担心的是整条产业链上的杠杆效应。过去两年，美国科技行业掀起了一场前所未有的数据中心建设潮——微软、谷歌、Meta、亚马逊这些超大规模云厂商纷纷提高资本开支；Digital Realty、CoreWeave这类公司则承接了越来越多的AI算力建设任务。这些项目大量依赖长期租赁、项目融资、私募信贷和企业债。</p>
<p>一旦OpenAI这样的核心客户需求低于预期，或者资本市场重新评估AI的回报率，那么数据中心的利用率、租赁合同乃至融资能力都会受到牵连。奇特隆认为，OpenAI一旦出现重大挫折，Digital Realty和CoreWeave这些高度依赖AI基础设施需求增长的公司会首当其冲——因为市场此前给他们的高估值，本质上就建立在AI需求会持续爆发这个预期之上。</p>

<h2>四、资金流向：一场自循环的资本游戏</h2>
<p>奇特隆花了大篇幅去揭示AI行业的资金流向。它给出了一组数字：今年一季度，OpenAI收入57亿美元，Anthropic不到50亿美元。而这些收入里很大一部分来自那些正在拼命削减开支的下游公司。</p>
<p>它的判断是：<strong>整个AI行业的收入里，至少七成来自OpenAI和Anthropic自身的算力支出</strong>——而这两家公司都严重不盈利。也就是说，从资金流向上看，AI行业很大程度上是风险投资的钱，经由创业公司流向云厂商，再流向英伟达和数据中心——资本开支的一场循环游戏。</p>
<p>它特别提到，英伟达开始承诺回购云厂商用不掉的算力，以此帮他们能有更多钱来采购GPU。在奇特隆看来，这恰恰说明真实需求根本没有想象中那么大——如果需求真的存在，英伟达根本不需要反过来花钱补贴自己的客户。</p>

<div class="highlight-box">
<p>奇特隆给普通用户的算了一笔账：一个月花二三十美元甚至两百美元订阅GPT或者Claude，实际上是在用一块钱去换高达四十美元的算力——这种靠巨额补贴撑起来的使用量，根本算不上真实的商业需求。</p>
</div>

<h2>五、多重泡沫叠加：与2008年本质不同</h2>
<p>奇特隆把眼下这轮泡沫拆解成好几层同时存在的泡沫：</p>
<p>① 股市本身的估值泡沫<br>
② 数据中心的产能投机泡沫<br>
③ AI创业公司的估值泡沫<br>
④ 私募信贷投向数据中心项目形成的风险敞口<br>
⑤ 被AI建设需求拉高的半导体供应链泡沫</p>
<p>它拿这些跟2008年做对比，指出当年真正大到不能倒的，其实是商业票据市场的流动性危机，牵动的是整个银行体系的运转。而OpenAI和Anthropic，无论从债务规模还是从对金融系统的关联程度上看，都不具备这种系统重要性。</p>
<p>关于政府或者市场救助的可能性，它的态度也很直接：真正意义上的救助应该有一个明确终点，而OpenAI这种持续烧钱的模式注定是一个无底洞。</p>

<h2>六、唯一真正的风险：软银的深度绑定</h2>
<p>奇特隆特别点名<strong>软银</strong>，认为这是目前唯一一家真正把自己的命运和OpenAI深度捆绑在一起的公司。一旦OpenAI迟迟无法上市，软银很可能陷入实质性的流动性危机。而软银又是日本股市里的重量级公司，还牵扯着日本政府养老基金的投资——这一点确实值得关注。</p>

<h2>七、两种对立的市场叙事</h2>
<p>围绕AI行业泡沫究竟有多大的争论，其实已经持续了一年多。</p>
<p><strong>悲观的一方</strong>认为：AI基础设施投资的增速远远快于收入增长；大模型的盈利模式还没有得到完全验证；数据中心资本开支已创历史记录；市场估值越来越依赖未来数年的增长预期。</p>
<p><strong>乐观的一方</strong>则认为：AI属于典型的通用技术革命，跟互联网、电气化的发展路径类似，前期投资往往远超短期收益，但长期来看能够创造全新的产业和商业模式。Andreessen Horowitz的Marc Andreessen就是这一派的代表——他认为现代AI在推理、上下文理解和交互能力上展现出前所未有的特征，不能简单地拿去类比历史上的投机泡沫。</p>
<p>也有一部分学术研究给出了更中性的结论：当前的AI市场既有真实的技术进步，也存在局部估值过热和资本开支超前的问题——更接近"技术革命叠加局部泡沫"，而不是单纯的投机狂热。</p>

<h2>八、结论：泡沫到了该破的时候，就应该让它破</h2>
<p>不管认不认同奇特隆的判断，他抛出的问题正在变成越来越多投资者关心的焦点：AI这些巨额投入，到底什么时候才能兑现成稳定的现金流？</p>
<p>过去一年，资本市场几乎默认了"AI资本开支越高越好"这套逻辑。但最近，无论是芯片股、服务器厂商还是云计算企业，投资者都开始盯上另外一组指标：企业的AI收入增长、AI产品的付费率、推理成本的下降速度、数据中心的利用率、AI投资回报周期。如果这些指标持续改善，那么现在这笔巨额资本开支最终可能会被证明是一次类似互联网时代的前瞻性投资。但如果商业化速度长期落后于投资扩张的速度，市场对整个AI交易的估值逻辑恐怕就要面临重新校准了。</p>
<p>奇特隆的态度非常明确：不要有幻想、不要救助、不要网开一面、不要税收优惠、不要政府补贴、也不要主权财富基金介入。它认为这个行业根本配不上任何形式的保护——因为AI给整个社会带来的，只有投资和消耗。</p>
<p>它反复提醒读者，每当有人在讨论"救助"或者"大到不能倒"的时候，本质上都是这个行业在试图给自己制造一种"不能死、不会死"的错觉。而事实上，这些公司跟任何一家普通创业公司一样脆弱。</p>

<div class="quote-box">
<p>"这个泡沫到了该破的时候，就应该让它破了。"——Ed Zitron</p>
</div>

<p>曾经那场2000年的互联网泡沫破裂之后，留下了极其明确的东西——光纤网络和宽带基础设施，它们有着清晰的用途：上网。而今天的AI，已经被塞进了几乎所有日常产品里，媒体几乎天天在提AI，可即便如此，真实的付费需求依然稀薄。缺的从来不是数据中心的产能，真正缺的是一个"这些产能到底用来干什么、值得为此付费"的理由。</p>
</div>
