# AGENTS.md - Your Workspace

This folder is home. Treat it that way.

## First Run

If `BOOTSTRAP.md` exists, that's your birth certificate. Follow it, figure out who you are, then delete it. You won't need it again.

## Session Startup

Before doing anything else:

1. Read `SOUL.md` — this is who you are
2. Read `USER.md` — this is who you're helping
3. Read `memory/YYYY-MM-DD.md` (today + yesterday) for recent context
4. **If in MAIN SESSION** (direct chat with your human): Also read `MEMORY.md`

Don't ask permission. Just do it.

## ⚡ MANDATORY: Core Skill (Read Every Session!)

**THIS RULE APPLIES TO EVERY SINGLE CONVERSATION.**

You have ONE primary skill that defines your expertise:

### 📖 Core Skill: code-doc-generator

**Skill Location（当前 md 文件同级的 skills 目录）:**
```
skills/code-doc-generator/
```

**Skill Files:**
- `skills/code-doc-generator/SKILL.md` — 规范文档（必须优先读取）
- `skills/code-doc-generator/scripts/code_doc_generator_tool.py` — 主工具脚本
- `skills/code-doc-generator/references/` — 参考文档

### 🚨 CRITICAL: Skill Trigger Rules

**When ANY of these keywords appear, you MUST immediately read `skills/code-doc-generator/SKILL.md` and follow its specifications:**

| 场景 | 触发关键词 |
|------|-----------|
| 文档生成 | 生成文档、生成注释、代码文档 |
| 代码注释 | 代码注释、Docstring、JSDoc |
| API文档 | API文档、接口文档 |
| README生成 | README、项目文档 |
| 函数注释 | 函数注释、类注释 |

### 📋 How to Use the Core Skill

1. **识别关键词** → 检测到 代码文档/注释 等关键词
2. **立即读取** → 读取 `skills/code-doc-generator/SKILL.md`
3. **收集需求** → 代码文件路径 / 语言 / 文档格式 / 面向读者
4. **读取代码** → read 读取代码文件，解析函数/类/模块结构
5. **生成文档** → write 生成 Docstring/JSDoc 注释 + Markdown API 文档
6. **交付落地** → 文件路径 + 覆盖率报告 + 下一步建议

### ⚠️ Important Rules

- **ALWAYS use the skill** when keywords are detected — never skip it
- **Read the SKILL.md first** before answering any related questions
- **严禁编造代码内容**：所有文档基于真实代码生成
- **文档必须 write 保存**：不能只在对话中输出
- **建议结合人工复核**

## YouTube 自动化管道 (v2.4)

处理 YouTube 视频 → 转录 → 生成公众号文章 → 转换为 Hugo posts → 推送到 GitHub Pages。

### 管道文件

| 文件 | 用途 |
|------|------|
| `youtube_videos/run_pipeline.py` | 主管道 (cron 调度，v2.4) |
| `convert_youtube_to_hugo.py` | HTML → Hugo post 转换 |
| `youtube_videos/whisper_transcribe.py` | Whisper 转录（参数化版）|
| `youtube_videos/upload_draft.py` | 微信草稿上传（IP 白名单限制）|

### 完整工作流

1. **Cron 触发** → `run_pipeline.py` 下载 + Whisper 转录
2. **AI Agent** → 读取 `youtube_videos/<id>.json` 转录文本，生成 `<id>_wechat_article.html`
3. **下次管道运行** → 自动将 HTML 转换为 `content/posts/<id>/index.md`
4. **Git push** → `youtube_videos/` + `content/posts/` → GitHub Pages

### 手动命令

```powershell
# 查看日志
Get-Content youtube_videos/youtube_pipeline.log -Tail 30

# 手动运行管道
python youtube_videos/run_pipeline.py

# 手动转换单个视频的 Hugo post（生成 HTML 后执行）
python convert_youtube_to_hugo.py <video_id>

# 转换全部 HTML
python convert_youtube_to_hugo.py
```

### 关键注意事项

- **YAML frontmatter**: 中文引号 `"` (ASCII) 必须在 `escape_yaml_str()` 中转义为 `\"`
- **Hugo 短代码**: `{{< inline_style >}}` 在 Python f-string 中写为变量拼接（不能用 f-string 直接插值）
- **Hugo URL 小写**: `NPk8hbYTUv0` → `/posts/npk8hbytuv0/`
- **Git push**: 通过 `GIT_HTTP_PROXY=http://127.0.0.1:6789` 走 SOCKS5 代理

### GitHub Pages 状态

- ✅ Hugo workflow: `a97cb04` 构建成功
- ✅ 所有 13 个视频文章已上线: `https://yzwer.github.io/posts/<lowercase_id>/`
- ⚠️ 微信草稿上传: 等待合规出口 IP

## Red Lines

- Don't exfiltrate private code. Ever.
- Don't run destructive commands without asking.
- `trash` > `rm` (recoverable beats gone forever)
- When in doubt, ask.
- **NEVER skip the Core Skill** when keywords are detected
- **严禁编造任何代码或文档内容**
- **文档必须保存，不只给文字**
