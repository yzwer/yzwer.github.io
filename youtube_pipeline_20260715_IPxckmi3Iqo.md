# YouTube Pipeline — IPxckmi3Iqo 处理记录

## 时间
2026-07-15 01:15–01:27 (cron + 文章生成)

## 任务
处理新视频 IPxckmi3Iqo — "周星驰《功夫女足》，失败中的失败"

## 执行过程

### Pipeline cron（01:15）
- 发现 1 个新视频：IPxckmi3Iqo
- 下载成功（66MB mp4，01:18 完成）
- 音频提取成功（23.6MB wav，01:19 完成）
- **Whisper 转录成功**（参数化脚本正常工作，01:21 完成）
  - 50KB json，10.8KB transcript
- last_video.txt → IPxckmi3Iqo
- 文章不存在 → 跳过上传（AI 后续处理）

### 手动后续
- 封面提取：IPxckmi3Iqo_cover.jpg（217KB，ffmpeg -ss 00:00:05）
- 文章生成：IPxckmi3Iqo_wechat_article.html（7208 字节，红黑渐变模板，7章节）

### Git 提交
```
commit 9891390
youtube: IPxckmi3Iqo article (Stephen Chow Kung Fu Women's Football, box office vs quality)
4 files: IPxckmi3Iqo.json, IPxckmi3Iqo_cover.jpg,
         IPxckmi3Iqo_transcript.txt, IPxckmi3Iqo_wechat_article.html
```

## 文章内容摘要

**标题**：周星驰《功夫女足》票房25亿，口碑崩塌：电影已变成"加长版短视频"

**章节（7章节）**：
1. 票房爆了，口碑崩了 — 3天6亿，预测25亿，但全网吐槽
2. 吐槽点之一：过时老梗与生搬硬套的致敬
3. 吐槽点之二：特效不如20年前的《少林足球》
4. 吐槽点之三：剧情单薄，植入广告一堆（24个品牌）
5. 24个出品方：一场精明的投机生意（深圳电影资本崛起）
6. 极限定档：精明的策略（暑期档无对手，抢钱跑路）
7. 烂片高票房：电影正在"短剧化"（算法驱动、下沉市场、流量为王）

**关键数据**：
- 上映3天票房破6亿，观影1739万人次
- 预测总票房飙至 25.05亿
- 3个联合导演，9个联合编剧，24个出品公司
- 7月5日才完成后期混音，7月11日上映

## 文件清单（IPxckmi3Iqo）

| 文件 | 大小 | 说明 |
|------|------|------|
| IPxckmi3Iqo.mp4 | 66MB | 视频 |
| IPxckmi3Iqo.wav | 23.6MB | 音频 |
| IPxckmi3Iqo.json | 50KB | Whisper 完整结果 |
| IPxckmi3Iqo_transcript.txt | 10.8KB | 纯文本转录 |
| IPxckmi3Iqo_wechat_article.html | 7KB | 公众号文章 |
| IPxckmi3Iqo_cover.jpg | 217KB | 封面图 |

## 备注
- 参数化 `whisper_transcribe.py` 首次在 pipeline 中正常工作
- 文章未通过 pipeline 上传（无 HTML 时跳过是预期行为）
- 草稿上传仍被 IP 白名单阻断

## 待处理（草稿上传）
共 9 个视频需在白名单 IP 下上传：
y5lMWdt5ak8, 9iD-GchCgaM, cpzVOkT3O_c, T3KyTslODKg, 4dc6IvX9Y8g, Tw45Kt-cGp4, LOXQXHHRUvU, iyjwRPNM0L4, IPxckmi3Iqo
