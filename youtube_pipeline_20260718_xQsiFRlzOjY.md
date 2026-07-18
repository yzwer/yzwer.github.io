# YouTube Pipeline — xQsiFRlzOjY 处理记录

## 时间
2026-07-18 01:16–01:33 (cron + 手动处理)

## 任务
处理新视频 xQsiFRlzOjY — "Destined to Collapse: The Next 'Lehman Brothers'?"

## 执行过程

### Pipeline cron（01:16）
- 发现 1 个新视频：xQsiFRlzOjY
- 下载启动但被 exec 300s SIGKILL 中断（01:21），仅 42MB .part 文件
- last_video.txt 未更新（仍为 PWUXT-Ohntk）

### 手动处理
- 手动 yt-dlp 下载成功：56.7MB mp4 + 11.9MB audio（01:21–01:23）
- 音频文件已存在（24.8MB wav）
- Whisper 转录成功：base 模型，4173 chars，386 segments（01:25–01:27）
- 封面提取：113KB（01:28）
- 文章生成：xQsiFRlzOjY_wechat_article.html（7782 字节，8 章节）
- last_video.txt → xQsiFRlzOjY

### Git 提交
```
commit 3570ce6
youtube: xQsiFRlzOjY (AI泡沫——OpenAI可能是下一个雷曼兄弟)
5 files: last_video.txt, xQsiFRlzOjY.json, xQsiFRlzOjY_transcript.txt,
         xQsiFRlzOjY_cover.jpg, xQsiFRlzOjY_wechat_article.html
```

## 文章核心内容

**标题**：AI时代的雷曼兄弟？深度拆解OpenAI泡沫论

**来源**：Ed Zitron 万字长文核心观点

**8 章节**：
1. 万字长文引爆AI业：OpenAI＝AI时代的雷曼兄弟
2. 商业模式三重缺陷（推理成本、资本开支、外部融资）
3. 比OpenAI更危险的是整条产业链的杠杆
4. 资金流向：一场自循环的资本游戏（7成收入来自自身算力支出）
5. 多重泡沫叠加（5层泡沫 vs 2008年本质不同）
6. 唯一真正的风险：软银与OpenAI深度绑定
7. 乐观与悲观的市场叙事对立
8. 结论：泡沫到了该破的时候就应该让它破

**关键数据**：
- OpenAI Q1收入57亿美元，Anthropic不到50亿——都不盈利
- 行业收入至少7成来自这两家公司自身的算力支出
- 用户每花1美元订阅，对应约40美元算力成本补贴
- 英伟达回购云厂商用不掉的算力（真实需求没想象中大）

## 备注
- 因 pipeline 300s 超时中断下载，手动完成全部流程
- 此文章涉及AI行业系统性风险分析，观点尖锐

## 待处理（草稿上传）
共 12 个视频需在白名单 IP 下上传微信草稿
