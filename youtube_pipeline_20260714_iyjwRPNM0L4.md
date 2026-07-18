# YouTube Pipeline — iyjwRPNM0L4 处理记录

## 时间
2026-07-14 01:15–01:38 (cron + 手动转录/文章)

## 任务
处理新视频 iyjwRPNM0L4 — "Huawei's 'Golden Child' is Running on Fumes"（赛力斯问界半年巨亏）

## 执行过程

### Pipeline cron（01:15）
- 发现 1 个新视频：iyjwRPNM0L4
- 下载成功（187MB mp4）
- 音频提取成功（24.7MB wav）
- Whisper 转录失败（exec timeout 300秒杀死进程 — 不是 OOM）
- last_video.txt 未更新（被 kill 前未完成）

### 修复 + 手动转录
1. 发现 `whisper_transcribe.py` 硬编码为 LOXQXHHRUvU（不接受参数）
2. 重写为通用版：接受 `<wav> <json> <model> <lang>` 参数
   - 注意：pipeline 调用格式 `python whisper_transcribe.py "{wav}" "{video_id}.json" base zh`
3. 手动运行：`python -u whisper_transcribe.py iyjwRPNM0L4.wav iyjwRPNM0L4.json base zh`
   - 语言检测：zh（置信度 100%）
   - 结果：3733 字符，317 segments
   - 耗时约 15 分钟（base 模型，CPU）

### 其他文件
- last_video.txt → iyjwRPNM0L4
- 封面：iyjwRPNM0L4_cover.jpg（272KB，ffmpeg -ss 00:00:05）
- 文章：iyjwRPNM0L4_wechat_article.html（8355 字节，红黑渐变模板，8章节）

### Git 提交
```
commit d14058e
youtube: iyjwRPNM0L4 article (Seres/Huawei AITO H1 loss) + parameterized whisper script
5 files: iyjwRPNM0L4.json, iyjwRPNM0L4_transcript.txt,
         iyjwRPNM0L4_wechat_article.html, iyjwRPNM0L4_cover.jpg, whisper_transcribe.py
```

## 文章内容摘要

**标题**：华为"金儿子"快没油了：赛力斯半年预亏15-18亿，问界神话正在褪色

**副标题**：7月12日晚赛力斯发布2026半年报预亏公告，归母净亏损15-18亿；问界汽车单季亏19-21.5亿；车越卖越多、钱越亏越多——华为智选车模式的"租金"到底有多贵？

**章节（8章节）**：
1. 一份炸裂的业绩预告：从盈利29亿到亏损18亿
2. 钱去哪了？藏在采购账单里的"华为税"
3. 高毛利低净利：卖38万的车，14万是华为的
4. 审计风暴与减值计提：M7换代的"后遗症"
5. 护城河消失：问界不再是华为的"独子"
6. 股价雪崩：一年蒸发1300亿市值
7. 两代接力与两条腿走路（AIVA新品牌 + 115亿收购引望）
8. 行业警示：价格战下的利润绞杀

**关键数据**：
- 上半年归母净亏损 15-18亿（去年盈利 29.4亿），落差 44亿
- 问界汽车单季亏 19-21.5亿
- 2025年向华为支付采购费 223.35亿，每辆车分给华为约 5.23万
- 问界单车均价 38万，其中 14万流向华为（占 35%+）
- 毛利率 29.14% 但净利率仅 3.72%
- 2026年1-2月营收 257亿（+34%），扣非净利仅 1.03亿（-73.87%）
- 股价一年蒸发约 1300亿市值
- 新品牌 AIVA：重庆国资 34.5% + 赛力斯 33% + 宁德时代 9.9%

## 待处理

### 草稿上传（需合规 IP）
以下 8 个视频的文章已生成，需在白名单 IP 下上传草稿：
- y5lMWdt5ak8（deleverage warning）
- 9iD-GchCgaM（real estate / AI wealth）
- cpzVOkT3O_c（美伊霍尔木兹海峡冲突）
- T3KyTslODKg（高善文去世）
- 4dc6IvX9Y8g（杨有林贪腐案）
- Tw45Kt-cGp4（6月 PPI/CPI 数据）
- LOXQXHHRUvU（亚速海无人艇攻击）
- iyjwRPNM0L4（赛力斯问界半年巨亏）← 本次新增

## 文件清单（iyjwRPNM0L4）

| 文件 | 大小 | 说明 |
|------|------|------|
| iyjwRPNM0L4.mp4 | 187MB | 视频 |
| iyjwRPNM0L4.wav | 24.7MB | 音频 |
| iyjwRPNM0L4.json | 39KB | Whisper 完整结果 |
| iyjwRPNM0L4_transcript.txt | 13KB | 纯文本转录 |
| iyjwRPNM0L4_wechat_article.html | 8.2KB | 公众号文章 |
| iyjwRPNM0L4_cover.jpg | 272KB | 封面图 |

## 备注
- `whisper_transcribe.py` 现已通用化，后续视频无需修改即可复用
- 注意：exec 调用 Whisper 时 timeout 不可设太低（base 模型约 15分钟）；建议单独后台运行或提高 timeout
