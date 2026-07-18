# YouTube Pipeline — LOXQXHHRUvU 处理记录

## 时间
2026-07-13 01:19–01:38 + 13:16 pipeline cron

## 任务
修复 LOXQXHHRUvU Whisper 转录失败 → 生成公众号文章 → 提交 git

## 问题排查

### Whisper 转录两次失败
- 原脚本 `whisper_transcribe.py` 使用 `import whisper`（openai-whisper），QClaw Python 环境无此模块
- 管道注释说"使用 faster-whisper"，但脚本实际使用 openai-whisper
- medium 模型下载 1.4GB 后加载超时（进程内存 ~1.5GB 不增长，被 OOM killer 终止）

### 修复方案
1. 安装 `faster-whisper`：`pip install faster-whisper`
2. 重写 `whisper_transcribe.py` 使用 `from faster_whisper import WhisperModel`
3. 模型从 `medium` 降级为 `base`（避免 CPU OOM）
4. 所有 print 加 `flush=True`（PowerShell 输出缓冲问题）

## 执行结果

### 转录
- 模型：`base`（Systran/faster-whisper-base，已缓存 ~138MB）
- 语言：英语（置信度 100%）
- 时长：~15分钟（模型加载 ~1min，推理 ~13min）
- 结果：13090 字符原文，251 segments
- 文件：
  - `LOXQXHHRUvU.json` — 完整 segments JSON
  - `LOXQXHHRUvU_transcript.txt` — 纯文本转录

### 公众号文章
- 文件：`LOXQXHHRUvU_wechat_article.html`（8629 字节）
- 标题：**亚速海突袭战：6天击沉72艘俄油轮，乌克兰如何用万元无人机拖垮超级大国**
- 副标题：7月6日至11日，乌无人艇在亚速海持续攻击俄影子舰队；6天内72艘油轮被命中；俄罗斯被迫暂停两条关键运输航线；无人机2万美元 vs 防空导弹200万美元的交换比逆转战局
- 章节（7章节）：
  1. 震惊世界的六天：28艘俄舰同时被命中
  2. 影子舰队：俄罗斯的"海上生命线"
  3. 从加油站到亚速海：乌克兰的"能源绞杀战"
  4. 防空困境：为什么俄罗斯"防不住"无人机？
  5. 交换比逆转：2万美元的无人机 vs 200万美元的导弹
  6. 电子战博弈：俄罗斯"波奇防护者"能反制吗？
  7. 三年三场大考：乌克兰的"成本逆转"战略
  8. 结语：小国的非对称战争范式

### 封面
- 文件：`LOXQXHHRUvU_cover.jpg`（170KB）
- 提取：ffmpeg -ss 00:00:05 -vframes 1 -update 1

### Git 提交
```
commit a080148
youtube: LOXQXHHRUvU article (Ukraine naval drone / shadow fleet attacks)
5 files: LOXQXHHRUvU.json, LOXQXHHRUvU_cover.jpg, LOXQXHHRUvU_transcript.txt,
         LOXQXHHRUvU_wechat_article.html, whisper_transcribe.py
```

### Pipeline cron（13:16）
- 发现 1 个新视频（LOXQXHHRUvU）
- 下载/音频/转录均跳过（已存在）
- last_video.txt 更新为 LOXQXHHRUvU
- 草稿上传失败（IP 白名单，预期行为）

## 待处理

### 草稿上传（需合规 IP）
以下 7 个视频的文章已生成，需在白名单 IP 下上传草稿：
- y5lMWdt5ak8（deleverage warning）
- 9iD-GchCgaM（real estate / AI wealth）
- cpzVOkT3O_c（美伊霍尔木兹海峡冲突）
- T3KyTslODKg（高善文去世）
- 4dc6IvX9Y8g（杨有林贪腐案）
- Tw45Kt-cGp4（6月 PPI/CPI 数据）
- LOXQXHHRUvU（亚速海无人艇攻击）← 本次新增

### whisper_transcribe.py 统一修复
- 现有脚本使用 `import whisper`（不兼容）
- 应统一使用 `from faster_whisper import WhisperModel`
- 可将 `whisper_transcribe.py` 改为通用模板（接收参数 video_id）

## 文件清单（LOXQXHHRUvU）

| 文件 | 大小 | 说明 |
|------|------|------|
| LOXQXHHRUvU.mp4 | 82MB | 视频 |
| LOXQXHHRUvU.wav | 21MB | 音频 |
| LOXQXHHRUvU.json | 39KB | Whisper 完整结果 |
| LOXQXHHRUvU_transcript.txt | 13KB | 纯文本转录 |
| LOXQXHHRUvU_wechat_article.html | 8.6KB | 公众号文章 |
| LOXQXHHRUvU_cover.jpg | 170KB | 封面图 |
