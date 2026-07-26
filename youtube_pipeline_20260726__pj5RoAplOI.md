# YouTube 视频流水线任务记录

**视频 ID**: _pj5RoAplOI  
**视频标题**: "Going Global Is a Minefield for Businesses" (企业出海，全是雷区)  
**发现时间**: 2026-07-26 13:17 (cron 第二次运行)  
**处理时间**: 2026-07-26 13:23–15:30 (管道下载失败，手动重试完成全流程)

---

## 任务执行记录

| 步骤 | 状态 | 详情 |
|------|------|------|
| 新视频发现 | ✅ | cron 检测到 1 个新视频 (last_video.txt=9cjVxjg9mAE) |
| 管道自动下载 | ❌ | SOCKS5 代理 3 次 rc=1 失败 (端口/SSL 抖动) |
| 管道 commit | ✅ | `4ff534c` (状态提交，last_video.txt 未更新，push 成功) |
| 手动下载(音频) | ✅ | HTTP 代理(6789)断点续传，音频流 f251.webm 16.99MB 100% 完成 |
| 手动下载(视频) | ⚠️ | 视频流 f399.mp4 因 SSL EOF 中断于 42.6% (122MB)，未完整 |
| 音频提取 | ✅ | ffmpeg 从 f251.webm 提取 wav 33.5MB (17分27秒) |
| Whisper 转录 | ✅ | base 模型，5141 字 / 505 段 / 中文 (概率1.00) |
| 文章生成 | ✅ | `_pj5RoAplOI_wechat_article.html` 9215 字节，10章节 |
| Hugo 转换 | ✅ | `content/posts/_pj5RoAplOI/index.md` 8221 字节 |
| 封面提取 | ✅ | 从部分视频流(.part)提取 `_pj5RoAplOI_cover.jpg` 97KB |
| last_video.txt | ✅ | 更新为 `_pj5RoAplOI` (无 BOM，绝对路径写入) |
| Git commit+push | ✅ | 文章+transcript+json+hugo+last_video+cookies 提交并推送 |
| 封面 commit+push | ✅ | 封面单独提交并推送 |

---

## 产物文件

| 文件 | 大小 | 备注 |
|------|------|------|
| `youtube_videos/_pj5RoAplOI_wechat_article.html` | 9215 bytes | 公众号文章，10章节 |
| `youtube_videos/_pj5RoAplOI_transcript.txt` | 14439 bytes | Whisper 转录 (UTF-8) |
| `youtube_videos/_pj5RoAplOI_cover.jpg` | 97 KB | 封面 (从部分流提取) |
| `youtube_videos/_pj5RoAplOI.wav` | 33.5 MB | 音频 (.gitignore 排除) |
| `youtube_videos/_pj5RoAplOI.json` | ~52 KB | Whisper 原始 JSON |
| `youtube_videos/_pj5RoAplOI.f251.webm` | 17.8 MB | 音频流 (下载完成) |
| `youtube_videos/_pj5RoAplOI.f399.mp4.part` | 122 MB | 视频流 (仅42.6%，未完整) |
| `youtube_videos/_pj5RoAplOI.f140.m4a` | 16.9 MB | 音频流 (管道第一次尝试) |
| `content/posts/_pj5RoAplOI/index.md` | 8221 bytes | Hugo post |

---

## 文章核心论点（公众号文章：欧盟5.5亿欧元天价罚单背后：中国跨境电商的黄金时代正在终结）

标题副标：速卖通、Temu、SHEIN两月内接连被重罚，四招监管组合拳精准踩中软肋——企业出海，遍地都是雷区

1. **5.5亿欧元创纪录罚单**：7月20日欧盟对阿里全球速卖通开5.5亿欧元罚单（DSA生效以来最高），理由：仿冒/高仿/不合规商品持续推送数周才下架、商家改分类躲合规、品牌授权人手不足、换链接照卖、1.93亿欧洲用户、10月20日前交整改方案
2. **非孤立事件**：5月28日Temu被罚2亿+匈牙利2000万；SHEIN法国累计2.1亿（虚假打折/隐私追踪/夸大宣传）；两月内三大出海电商巨头接连被重罚
3. **后门起源**：2008年欧盟为海关减负推150欧以下小包裹免税，无意给中国跨境电商开高速后门；2023巅峰期进入欧盟小额免税包裹23/46/59亿件（9成中国，每秒140包裹）
4. **第一招 灵活解释权**：VLOP标准要求识别"系统性风险"但无明确定义，解释权握在欧委会手中，操作空间巨大
5. **第二招 关税大棒**：7月1日取消150欧免税，每件征3欧固定关税+分商品分别计税，砍掉小包裹直邮价格优势
6. **第三招 国家主体针对性立法**：法国反超快时尚法案，最高5欧/件生态税+禁广告（含网红营销/免费配送宣传），广告被断=判死刑
7. **第四招 线上线下一锅端**：DSA砍线上，FSI外国补贴条例砍线下（京东收购德国Ceconomy被查）；FSI反转举证——"我怀疑你拿补贴，自证清白的是你"
8. **动了谁的蛋糕**：2025欧盟对华逆差3600亿欧(+15%)、27国全逆差；欧洲零售机器跑半世纪，零售批发占GDP10%、2600万就业、500万企业；近5年中国跨境占平价零售92%增量，中小经销商倒闭3.8万、闭店1.2万；税基流失（取消免税后年增几百亿欧）
9. **不止电商**：TikTok/DJI/小米/Smoore/阿里/腾讯/三一各行业在欧美东南亚挨罚；根因是把国内"二选一"、控价、先规模后合规老路照搬海外成雷区
10. **黄金时代终结**：全球同步收严，合规边界模糊执法主观，天价罚单吃掉数年利润，中小卖家日子难过，进入高风险低增长新周期，出海路上雷越来越多

---

## 已知问题

- 管道 SOCKS5 代理(6789)本日不稳定，3次下载全败；改用 HTTP 代理(6789)手动续传完成（仍偶发 SSL EOF）
- 视频流 f399.mp4 未完整下载（42.6%中断），封面系从部分流提取，如后续需完整视频可续传
- 所有草稿上传仍因出口 IP 白名单（errcode 40164）阻塞

---

## Git 提交记录

```
<main commit> 9cjVxjg9mAE done; _pj5RoAplOI: EU fines China cross-border ecommerce, 10-ch article + Hugo post
<cover commit> _pj5RoAplOI: add cover (extracted from partial stream)
4ff534c (来自13:22 cron) youtube: pipeline run 2026-07-26 13:22 + Hugo posts
```

**远程仓库**: `https://github.com/yzwer/yzwer.github.io.git` (HTTPS, 带 token)  
**网站 URL**: `https://yzwer.github.io/posts/_pj5roaploi/` (视频ID含前导下划线，URL小写化)
