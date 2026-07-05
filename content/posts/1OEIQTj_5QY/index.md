---
title: "华为\"掏定律\"真相：技术创新还是营销包装？"
date: 2026-05-27
draft: false
description: "从摩尔定律到\"掏定律\"——为什么业内的反应如此强烈"
tags:
  - "深度分析"
  - "华为"
  - "摩尔定律"
  - "半导体"
---

{{< inline_style >}}
/* 主题's .content 内文章内容样式 */
/* 作用域：主题默认在 .content 内渲染，selectors 无需额外wrapper */

/* 子标题 */
h2 {
    font-size: 20px;
    color: #1a3a5c;
    margin: 30px 0 18px;
    padding-bottom: 10px;
    border-bottom: 2px solid #e8f0f8;
    font-weight: 600;
}

h2:first-child { margin-top: 0; }

/* 段落 */
p {
    font-size: 16px;
    margin-bottom: 16px;
    text-align: justify;
    line-height: 1.8;
    color: #333;
}

/* 高亮框 */
div.highlight-box {
    background: #fff8e1;
    border-left: 4px solid #ffc107;
    padding: 18px 20px;
    margin: 24px 0;
    border-radius: 0 6px 6px 0;
}

.highlight-box p {
    margin: 0;
    color: #5d4e00;
    font-weight: 500;
}

div.highlight-blue {
    background: #e3f2fd;
    border-left: 4px solid #1565c0;
    padding: 18px 20px;
    margin: 24px 0;
    border-radius: 0 6px 6px 0;
}

.highlight-blue p {
    margin: 0;
    color: #0d47a1;
}

/* 数据网格 */
div.data-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
    margin: 20px 0;
}

.data-card {
    background: #f0f4f8;
    padding: 15px;
    border-radius: 6px;
    text-align: center;
}

.data-card .number {
    font-size: 22px;
    font-weight: 700;
    color: #c62828;
}

.data-card .label {
    font-size: 13px;
    color: #666;
    margin-top: 4px;
}

/* 数据框 */
div.data-box {
    background: #f8f9fa;
    padding: 20px;
    border-radius: 8px;
    margin: 20px 0;
    border: 1px solid #e9ecef;
}

.data-box h3 {
    font-size: 16px;
    color: #495057;
    margin-bottom: 12px;
}

/* 警告框 */
div.warning-box {
    background: #fff3cd;
    border: 1px solid #ffc107;
    border-radius: 8px;
    padding: 20px;
    margin: 25px 0;
}

.warning-box strong { color: #856404; }

/* 步骤框 */
div.step-box {
    background: #fafafa;
    border: 1px solid #e0e0e0;
    border-radius: 6px;
    padding: 16px;
    margin: 12px 0;
}

.step-box .step-title { font-weight: 700; color: #0d47a1; }

/* 表格 */
table {
    width: 100%;
    border-collapse: collapse;
    margin: 20px 0;
    font-size: 15px;
}

table th {
    background: #1a3a5c;
    color: #fff;
    padding: 10px 12px;
    text-align: left;
}

table td {
    padding: 10px 12px;
    border-bottom: 1px solid #e9ecef;
}

table tr:last-child td { border-bottom: none; }

/* 强调 */
strong { color: #1565c0; }

span.warning { color: #c62828; font-weight: 600; }

/* 分割线 */
.section-divider {
    height: 1px;
    background: linear-gradient(to right, transparent, #e0e0e0, transparent);
    margin: 30px 0;
}

/* 移动端适配 */
@media (max-width: 768px) {
    div.data-grid { grid-template-columns: 1fr; }
    h2 { font-size: 18px; }
    p { font-size: 15px; }
}

{{< /inline_style >}}

<div class="lead">
华为最近搞了个大活，提出"掏定律"，说要取代摩��定律，引发了很大争议。今天我们来好好聊一聊，这里面究竟有什么问题。
</div>
<div class="st"><div class="sn">1</div><div class="stx">摩尔定律到底是什么？——为什么整个行业把它当"圣经"</div></div>
<p>先从最基础的说起。摩尔定律这个名字，大家可能听过很多次——<strong>简单讲，就是芯片上的晶体管数量大概每两年翻一倍，性能跟着翻，功耗跟着降，成本也会跟着下降</strong>。</p>
<p>这个规律从上世纪60年代提出来，一路验证了几十年，是整个半导体行业发展的核心逻辑。</p>
<p>那怎么做到晶体管数量翻倍的呢？就是我们平时听到的<strong>28纳米、14纳米、7纳米、5纳米</strong>——指的就是晶体管的特征尺寸。数字越小，单位面积能塞进去的晶体管就越多，性能就越强。</p>
<p>现在台积电已经在量产<strong>3纳米</strong>芯片，2纳米也已经规划量产了，苹果、英伟达这些大客户都在排队等着。</p>
<p><strong>但是，问题就来了——说到这个程度，已经快碰到物理极限了</strong>。晶体管小到一定尺寸，会出现一个很严重的问题，叫做<strong>"量子隧穿效应"</strong>。</p>
<div class="ic">
<h4>🔬 量子隧穿效应：摩尔定律的"终场哨"</h4>
<ul>
<li>正常情况下，晶体管就像一个开关：你控制它开，电子才能通过；你控制它关，电子就不能通过</li>
<li>但当晶体管小到几纳米的时候，<strong>电子会不受控制地直接"穿墙而过"</strong>——根本不管你开关有没有打开</li>
<li>这就导致<strong>大量漏电、运算出错，根本没法用</strong></li>
</ul>
</div>
<p>所以很多人都在说：<strong>摩尔定律走到头了，行业进入了"后摩尔时代"</strong>。</p>
<div class="st"><div class="sn">2</div><div class="stx">华为的"掏定律"：到底在讲什么？</div></div>
<p>而最近，华为海思的总裁何廷波在一个国际半导体会议上发布了<strong>"掏定律"</strong>。"掏"这个字，取的是希腊字母"τ"的音译，中文叫什么……em……"掏"有点掏光养慧的意思，名字起得挺有意思的。</p>
<p>那掏定律的核心思想是什么呢？</p>
<p>何廷波在论文里写了一句话，原文是英文，翻译过来就是：<strong>"本质上，每一代技术进步实现的，是时间的减少。"</strong></p>
<p>这句话是整个掏定律的核心——意思是说：我们以前理解的芯片性能提升，本质不是晶体管变小，<strong>而是芯片完成任务的时间在缩短</strong>。晶体管变小，只是让时间缩短的其中一种方式，而不是唯一方式，更不是以后唯一的路。</p>
<p>打个比方：芯片是一座城市，城市里的居民是数据。摩尔定律的思路是：把楼盖得越来越高，建筑密度越来越大，把地皮利用到极限——现在地皮快用完了，楼没办法再盖了，摩尔定律就遇到了瓶颈。</p>
<p><strong>掏定律的思路是说：换个角度，不盖楼了，改修地铁、修高架，优化交通网络，让数据在城市里跑得更快、更顺畅，同样能解决居住效率的问题</strong>。</p>
<div class="st"><div class="sn">3</div><div class="stx">四个层面的"时间压缩"方案</div></div>
<p>具体来说，华为提出从四个层面来降低芯片完成任务的时间：</p>
<div class="ic">
<h4>📐 华为的四大技术方向</h4>
<ul>
<li><strong>第一层：晶体管层面</strong>——通过提升栅氧，采用高K金属栅极等手段，降低晶体管本身的开关延迟</li>
<li><strong>第二层：电路层面</strong>——通过垂直互连，采用低电阻导体等方式，降低信号在电路里传播的延迟</li>
<li><strong>��三层：芯片架构层面</strong>——通过重新设计计算逻辑和内存结构，降低计算和内存访问的延迟</li>
<li><strong>第四层：系统层面</strong>——通过改进不同芯片之间的互联方式，降低整个系统的通信延迟</li>
</ul>
</div>
<p>在这个思路下，华为提出了几个具体的技术方案。最重要的一个叫<strong>"Logic Folding"</strong>，中文叫"逻辑折叠"。传统芯片的晶体管是平铺在一个平面上的，就像一层楼里摆了很多桌子；逻辑折叠的思路，是把这些晶体管立体地堆叠起来，A和B两个晶体管原来在同一平面信号只能先经过A再到B，现在把它们上下叠在一起，信号可以同时到达A和B，<strong>传输时间直接缩短</strong>。</p>
<p>华为宣布：用了逻辑折叠技术之后，2026年即将发布的新麒麟芯片，晶体管密度从每平方毫米155万个，提升到238万个，<strong>核心能效提升了41%，时钟频率提升了将近13%</strong>。</p>
<p>除了逻辑折叠，华为还提出了：</p>
<ul>
<li><strong>Unified Bus</strong>——用于人工智能数据中心的通信协议，把数据中心里不同芯片之间的访问延迟从几十微秒压缩到100微秒，<strong>差距是几百倍</strong></li>
<li><strong>Co-Packaged Optics (CPO)</strong>——也就是"封装光输入输出"，就是用光信号代替传统的电信号来传输数据，大幅降低延迟和功耗</li>
</ul>
<p>最终目标：华为说，到2031年，通过这一系列技术的叠加，实现<strong>等效1.4nm</strong>的性能水平。1.4nm是个什么概念？台积电现在量产的最先进工艺是3nm，2nm还在规划中——1.4nm更是遥遥无期。华为说要在2031年靠这套方法达到同等效果，<strong>野心相当大</strong>。</p>
<div class="st"><div class="sn">4</div><div class="stx">但是业内人士一看，问题和质疑就来了</div></div>
<p>先说技术本身。</p>
<p>华为提出的这些技术路线——3D堆叠、混合键合、先进封装、Chiplet互联优化——<strong>这些方向其实不是华为发明的，是整个半导体行业在后摩尔时代共同探索的路径，而且已经走了很多年了</strong>。</p>
<table>
<tr><th>年份</th><th>公司</th><th>技术突破</th></tr>
<tr><td>2012</td><td>索尼</td><td>开始量产堆叠式图像传感器</td></tr>
<tr><td>2015</td><td>索尼</td><td>发展出"童童直接键合"技术(hybrid bonding)</td></tr>
<tr><td>2017</td><td>索尼</td><td>提出三层堆叠方案</td></tr>
<tr><td>近年</td><td>台积电</td><td>用超高密度垂直堆叠做异构芯片，建键间距从Sub-10微米起步</td></tr>
<tr><td>近年</td><td>英特尔</td><td>Foveros Direct 3D，用hybrid bonding做到Sub-10微米的互联间距</td></tr>
</table>
<p>这些技术，跟华为宣传的"缩短传播延迟、提高有效密度"，说相似都是客气的了。</p>
<p><strong>当然，我们要公平地说：华为把这些技术系统化地整合在一起，应用到自己的芯片设计全链条里，这本身是有工程价值的，不是说完全没有贡献。</strong></p>
<p>但把这套整合工作包装成"自主创新定律"、改写全球规则——<strong>这个说法，确实有点让人绷不住了</strong>。</p>
<div class="st"><div class="sn">5</div><div class="stx">还有几个关键技术问题</div></div>
<p><strong>第一个问题："等效1.4nm"这个说法，内行人看了直接开喷。</strong></p>
<p>业界的共识是：晶体管密度的比较，必须是在同一张晶圆上做出来的才有意义。华为把两张芯片叠在一起，密度翻倍，然后说"等效1.4nm"——如果台积电把两张2纳米的芯片叠在一起，按华为的算法，性能岂不是要"秒杀一切"？</p>
<p><strong>第二个问题：堆叠以后的散热绕不开。</strong></p>
<p>晶体管密度增大、堆叠以后，热量更难散出去——升温以后，功耗又会进一步上升——这是一个恶性循环。在不改变晶体管工艺制成的前提下，动态功耗根本降不下来。堆叠以后的散热问题，可能得靠风冷、夜冷、液冷这些手段——<strong>华为在宣传里基本只字不提</strong>。</p>
<div class="st"><div class="sn">6</div><div class="stx">更核心的问题：悄悄混淆了两件事</div></div>
<p>其实 Huawei 这篇论文，还有个问题很多人没看出来——<strong>就是悄悄地，把两件不完全一样的事情混在了一起。</strong></p>
<p><strong>第一件事</strong>：摩尔定律在物理和经济层面都遇到了瓶颈，行业需要寻找新方向——这是真的业内共识，没有问题。</p>
<p><strong>第二件事</strong>：华为被美国制裁，拿不到EUV光刻机，进不了台积电的先进制程，只能在现有条件下另辟蹊径——这也是真的，但这是华为自己的问题，不是整个行业的处境。</p>
<p>这两件事有交叉，但不是同一件事。台积电的N2工艺在2025年底已经开始量产，A14节点也计划在2028年量产——相比N2还有15%的速度提升和30%的功耗降低，晶体管密度还在线性提升。摩尔定律的物理极限还没有真的��顶——<strong>只是"经济红利"确实在递减</strong>。</p>
<p><strong>华为的做法是：把我被制裁所以只能走这条路，包装成整个行业都走到了头，所以这条路是全行业的必然出路，而且是我率先指出来的。</strong></p>
<p>简单说就是：先用行业共识铺路，再让自己的解决方案显得是历史的必然、是唯一正确答案。</p>
<div class="st"><div class="sn">7</div><div class="stx">似曾相识的套路：5G的"前车之鉴"</div></div>
<p>说到这，我们必须讲<strong>5G这个例子</strong>，因为几乎是 <strong>一模一样的套路</strong>。</p>
<p>大家应该还记得，几年前华为高调宣布打通了5G技术，要全面商业推广——运营商跟进、政府大力支持、媒体铺天盖地说"中国5G领跑全球，要全面超越英美"，全国上下都很兴奋。</p>
<p>5G本身是个真实的技术毋庸置疑——高带宽、低延迟、大规模连接，是无线通信的未来，方向没有问题。但问题在于：华为当时推出的5G技术，其实<strong>并不完整</strong>。</p>
<div class="wc">
<h4>📱 5G的真实情况</h4>
<ul style="padding-left:20px;margin-top:10px;">
<li style="color:#555;line-height:2;">5G频段分低频、中频和高频毫米波三个部分，真正能实现那些让人激动的超低延迟和超高带宽的，是<strong>高频毫米波</strong>部分</li>
<li style="color:#555;line-height:2;">但华为当时的技术只能用低频段那一块，高频毫米波根本没有真正打通商用</li>
<li style="color:#555;line-height:2;">结果就是：虽然名义上用了5G频段，但实际提升对普通用户来说相当有限</li>
<li style="color:#555;line-height:2;">大部分人的日常体验确实比4G快一点，但远没有宣传里说得那么革命性</li>
</ul>
</div>
<p>然后发生了什么呢？大家应该有目共睹：</p>
<ul>
<li>运营商为了铺设5G基站投入了巨额资金，这个窟窿要填上，于是开始全力推销5G套餐，价格从100多到200块</li>
<li>同时后台对4G网络开始悄悄降速，让你感觉4G明显变慢——相比之下5G就显得更快了，让你不得不选</li>
<li>5G模式下流量的消耗也明显更多，运营商也喜欢——手机厂商也纷纷跟进，大量推出5G手机，用各种营销手段催促用户换机</li>
</ul>
<p><strong>普通用户稀里糊涂换了手机换了套餐，结果发现日常用的功能跟以前也没什么本质区别——就这样交了一轮不小的"智商税"。</strong></p>
<p><strong>而且整件事最让人无语的是</strong>：华为后来因为被制裁，自己做不了5G手机了，市场上突然出现了很多声音说"红蒙加4G好用过5G"——从当初捧5G捧得震天响，到后来暗示5G没什么了不起——前后打脸的速度之快，确实让人碳为观止。</p>
<div class="dv"></div>
<p>回过头来看，5G这件事的问题不是技术方向错了——方向是对的，5G确实比4G先进。但<strong>时机不成熟，并且可以夸大了效果，最后买单的只是普通老百姓</strong>。</p>
<p>再来看看"掏定律"，<strong>是不是感觉一模一样</strong>？</p>
<div class="st"><div class="sn">8</div><div class="stx">总结："掏定律"的价值与局限</div></div>
<p>总的来说，"掏定律"最有价值的地方，是选对了后摩尔时代的工程方向——不再在纳米级别上内卷，这一点值得肯定。</p>
<p><strong>但最讽刺的地方，其实也在这：把全行业都在走的方向，包装成自己首创的"新定律"，还用国际会议的形式发出来——营销能力确实一流。</strong></p>
<p>这种操作，暂时能提振士气、圈一波流量，但长期来看，如果技术落地效果没有宣传那么好，或者台积电、英特尔在先进制程上继续突破——那么这个"定律"，就会像5G一样，慢慢变成一个尴尬的记忆。</p>
<p>当然，话说回来，国内很多工程师是真的在认真做事，华为的工程团队能在受限条件下做到现在这个程度，确实不容易——可<strong>做事归做事，夸大宣传则是另一回事了</strong>。</p>
<p>这也许能让炒作的人很开心：因为又有概念可以炒作了，<strong>但也就仅此而已</strong>。这种做法短期看也许赢了舆论，但长期看是在不断消耗公信力。</p>
<div class="dv"></div>
<p style="color:#999;font-size:14px;text-align:right;">—— 基于YouTube视频内容整理分析</p>
