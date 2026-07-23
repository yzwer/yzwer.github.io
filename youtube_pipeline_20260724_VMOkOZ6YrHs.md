# YouTube 视频流水线任务记录

**视频 ID**: VMOkOZ6YrHs  
**视频标题**: "Under Intense Bombardment, Is It Reaching a Breaking Point?"  
**视频描述**: 乌克兰 vs 俄罗斯——无人机越打越多，俄炼油产能跌至21年最低，石油大国闹油荒，内阁大洗牌，财政窟窿600-800亿美元  
**发现时间**: 2026-07-24 01:15 (cron)  
**处理时间**: 2026-07-24 01:29

---

## 任务执行记录

| 步骤 | 状态 | 详情 |
|------|------|------|
| 新视频发现 | ✅ | `VMOkOZ6YrHs` |
| 下载 (SOCKS5) | ⚠️ | 管道第一次下载到 ~150MB 后 rc=1 失败，第2/3次重试均失败。`.f137.mp4.part` 160MB 残留 |
| 手动断点续传 | ✅ | `youtube-dl --continue` 恢复下载，成功（具体大小待确认） |
| 音频提取 | ✅ | `.m4a` 14.3MB (约15分钟)；`.f251.webm` 15MB |
| Whisper 转录 | ✅ | 4543 字 / 385 段 / 中文 |
| 封面提取 | ✅ | `VMOkOZ6YrHs_cover.jpg` 114.5KB |
| 文章生成 | ✅ | `VMOkOZ6YrHs_wechat_article.html` 9021 字节，9章节 |
| Hugo 转换 | ✅ | `content/posts/VMOkOZ6YrHs/index.md` 13140 字节 |
| Git commit | ✅ | `2acaa6d` (5 files: article, cover, transcript, json, Hugo post) |
| Git push | ✅ | `dff3a05..2acaa6d master -> master` (第1次 SSL 失败，第2次成功) |

---

## 产物文件

| 文件 | 大小 | 备注 |
|------|------|------|
| `youtube_videos/VMOkOZ6YrHs_wechat_article.html` | 9021 bytes | 公众号文章，9章节，红黑渐变模板 |
| `youtube_videos/VMOkOZ6YrHs_transcript.txt` | 12635 bytes | Whisper 转录文本（UTF-8） |
| `youtube_videos/VMOkOZ6YrHs_cover.jpg` | 114.5 KB | 视频封面 |
| `youtube_videos/VMOkOZ6YrHs.json` | ~52 KB | Whisper 原始 JSON |
| `content/posts/VMOkOZ6YrHs/index.md` | 13140 bytes | Hugo post |

---

## 文章核心论点（公众号文章）

1. **史上最大规模袭击**：7月20日一夜400+架无人机扑向俄领土，超远程打击400公里外的油库
2. **石油大国闹油荒**：俄6月日炼油量-25%至380-395万桶，创21年最低；国内批发价涨60%；40多个联邦主体燃油限购
3. **百万桶原油漂海上**：俄1.35亿桶原油滞留全球各港口（印度西海岸60%）；印度买家库存饱和+苏伊士运河排队
4. **炼油恢复遥遥无期**：老旧装置依赖欧美配件（制裁断供）；修复周期从6周拉长至6-9个月；中国标准不兼容短期无法援助
5. **乌克兰越打越强**：无人机年产能从80万（2023）→ 220万（2024）→ 400万（2025）→ 600-800万（2026预）；西方5年军援超900亿美元
6. **内阁大洗牌**：泽连斯基一周内撤换国防部长、总司令、总理——科技派 vs 传统派路线之争
7. **俄财政窟窿**：每天1亿美元损失（全年300亿）；进口成品油年50亿；修复炼油厂年100亿；总计600-800亿/年
8. **俄内部债务危机**：企业债务涨93%；个人破产Q1 13.75万（+14%）；真实不良贷款或达1536亿美元
9. **结语**：俄短期不崩，但若无人机攻势持续2-3年将被迫收缩战线

---

## 已知问题

- SOCKS5 代理（`127.0.0.1:7890`）不稳定，首次下载在 ~150MB 处 rc=1 失败
- `.f137.mp4.part` 残留 160MB，部分下载文件
- GitHub Pages 验证因网络代理问题暂时无法完成（已确认 push 成功）
- 所有草稿上传仍因出口 IP 白名单（errcode 40164）阻塞

---

## Git 提交记录

```
2acaa6d VMOkOZ6YrHs: 乌俄无人机炼油战，9章节公众号文章 + Hugo post (13KB)
dff3a05 (来自管道 cron) 4 files changed (ArvpXiBiK4U_transcript.txt 等)
```

**远程仓库**: `https://github.com/yzwer/yzwer.github.io.git` (HTTPS)  
**网站 URL**: `https://yzwer.github.io/posts/vmokoz6yrhs/` (URL 小写化)
