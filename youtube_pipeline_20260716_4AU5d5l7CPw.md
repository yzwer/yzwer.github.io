# YouTube Pipeline — 4AU5d5l7CPw 处理记录

## 时间
2026-07-16 01:15–01:28 (cron + 手动转录 + 文章生成)

## 任务
处理新视频 4AU5d5l7CPw — "紧急禁令，严重短缺"

## 执行过程

### Pipeline cron（01:16）
- 发现 1 个新视频：4AU5d5l7CPw
- 下载首尝试 rc=1 失败，重试成功（124MB mp4，01:19 完成）
- 音频提取成功（28.4MB wav，01:19 完成）
- Whisper 转录被 exec 300秒超时 SIGKILL 中断（仅 mp4/wav 存在，无 transcript）
  - 原因：cron 调用父进程 exec timeout 300秒，base 模型转录约需 8 分钟

### 手动修复
- 后台重跑 whisper_transcribe.py（background true, timeout 900）→ 成功
  - 4293 字符，371 段落，语言 zh (prob=1.00)
- 更新 last_video.txt → 4AU5d5l7CPw
- 封面提取：4AU5d5l7CPw_cover.jpg（184KB）
- 文章生成：4AU5d5l7CPw_wechat_article.html（9161 字节，红黑渐变模板，10章节）

### Git 提交
```
commit 28e48b1
youtube: 4AU5d5l7CPw article (China helium export ban, strategic resource crisis)
4 files: 4AU5d5l7CPw.json, 4AU5d5l7CPw_cover.jpg,
         4AU5d5l7CPw_transcript.txt, 4AU5d5l7CPw_wechat_article.html
```

## 文章内容摘要

**标题**：紧急禁令，严重短缺：中国为何突然全面禁止氦气出口？一场高端产业的自保战

**章节（10章节）**：
1. 一纸禁令：全球最大进口国，为何先"断供"自己？（商务部+海关公告，全品类禁出口）
2. 氦气到底是什么？为什么它无可替代？（战略稀有气体，无合成替代）
3. 三大命脉领域：芯片、医疗、航天（光刻控温、MRI超导、火箭加压）
4. 资源困局：全球90%的氦气集中在四国（美/卡/俄/阿）
5. 中国的尴尬：天然气大国，却是氦气贫国（2025产量905吨 vs 消耗6000吨，依存度>84%）
6. 2026年三重冲击：卡塔尔爆炸、俄罗斯管制、美国封锁（现货+490%，工业级80→170元/方）
7. 出口管制：一场不得已的自保战（出口仅占总供给7.6%，无国家级战略储备）
8. 破局之路：提氦技术与回收系统（自给率2022<5%→2025约15%，2026目标25%）
9. 日韩的至暗时刻：转口通道也被掐断（跨国巨头在华设实体规避制裁，现已断路）
10. 结语：震痛之后，是产业链的觉醒（40L瓶装3900-4800元 vs 年初550元，涨幅700%+）

**关键数据**：
- 中国2025氦气产量905吨，年耗近6000吨，对外依存度>84%
- 进口结构：卡塔尔55% + 俄罗斯43% = 98%（美国仅1%）
- 卡塔尔产能占全球30%+（爆炸致全球减供1/3）；俄罗斯配额压缩至40%
- 4月底高纯氦现货最高涨幅近490%；6N超高纯氦不在长期协议内
- 自给率目标：2026底>25%，2030>40%

## 文件清单（4AU5d5l7CPw）

| 文件 | 大小 | 说明 |
|------|------|------|
| 4AU5d5l7CPw.mp4 | 124MB | 视频（未提交，体积大） |
| 4AU5d5l7CPw.wav | 28.4MB | 音频（未提交，体积大） |
| 4AU5d5l7CPw.json | 50KB | Whisper 完整结果 |
| 4AU5d5l7CPw_transcript.txt | 11.9KB | 纯文本转录 |
| 4AU5d5l7CPw_wechat_article.html | 9KB | 公众号文章 |
| 4AU5d5l7CPw_cover.jpg | 184KB | 封面图 |

## 待处理（草稿上传）
共 10 个视频需在白名单 IP 下上传：
y5lMWdt5ak8, 9iD-GchCgaM, cpzVOkT3O_c, T3KyTslODKg, 4dc6IvX9Y8g, Tw45Kt-cGp4, LOXQXHHRUvU, iyjwRPNM0L4, IPxckmi3Iqo, 4AU5d5l7CPw
