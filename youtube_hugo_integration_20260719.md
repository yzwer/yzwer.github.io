# YouTube → Hugo 自动化管道集成

**日期**: 2026-07-19
**操作人**: 代码文学家 Agent

## 目标
将 YouTube 视频自动处理管道的产物（HTML 文章）自动转换为 Hugo 博客 posts 并推送到 GitHub Pages。

## 完成的变更

### 1. `convert_youtube_to_hugo.py`（完全重写）

**位置**: `C:\Users\11132\.qclaw\workspace-yw3plsutb1jupnif\convert_youtube_to_hugo.py`

**功能**:
- 读取 `youtube_videos/*_wechat_article.html`
- 解析 `<title>`、`<style>`（CSS）、`<div class="content">`（正文）
- 生成 `content/posts/<video_id>/index.md`（Hugo post 格式）

**关键修复**:
- ✅ 支持新格式 (`<div class="content">`) 和旧格式 (`<div class="container">`)
- ✅ Python f-string 中 `{{<` 短代码改为变量拼接（避免 `{{` 被解析为 f-string 转义）
- ✅ `escape_yaml_str()` 函数正确转义 YAML 双引号字符串中的 ASCII 双引号 `"`（U+0022）
  - 中文引号 `""` 是 ASCII 双引号，必须转义为 `\"`
  - 中文破折号 `——` 是 Unicode 字符（U+2014），不需要转义
  - 其他控制字符（`\n`, `\t`, `\r`）也正确处理

**用法**:
```bash
# 转换全部
python convert_youtube_to_hugo.py

# 只转换单个视频
python convert_youtube_to_hugo.py <video_id>
```

### 2. `run_pipeline.py`（v2.3 → v2.4）

**位置**: `C:\Users\11132\.qclaw\workspace-yw3plsutb1jupnif\youtube_videos\run_pipeline.py`

**新增功能**:
1. 处理完每个视频后，检查是否有对应的 HTML 文章
2. 若有，调用 `convert_youtube_to_hugo.py` 转换为 Hugo post
3. Git push 包含 `youtube_videos/` 和 `content/posts/` 两个目录

**新增代码段**:
```python
# Hugo: Convert any new HTML articles to Hugo posts
for v in reversed(to_process):
    vid = v['id']
    html_file = WORK_DIR / f"{vid}_wechat_article.html"
    if html_file.exists():
        _convert_html_to_hugo(vid, html_file, _repo_root)

# Git Push includes content/posts/
_sp2.run(["git", "add", "-A", "youtube_videos/", "content/posts/"], ...)
```

### 3. GitHub Actions / Hugo Workflow

**文件**: `.github/workflows/hugo.yml`
- Hugo 版本: 0.161.1（扩展版）
- 构建命令: `hugo --gc --minify --baseURL "${{ steps.pages.outputs.base_url }}/"`
- 部署到 GitHub Pages (master 分支)

### 4. Hugo Post 格式

```yaml
---
title: "标题（含中文引号需转义）"
date: 2026-07-19T01:22:50+08:00
draft: false
description: "描述文字"
---

{{< inline_style >}}
<style>...</style>
{{< /inline_style >}}

<body>...</body>
```

## 调试记录

### 问题1: Python f-string `{{` 被转义
- **现象**: `{{< inline_style >}}` 在输出文件变为 `{< inline_style >}}`
- **根因**: Python f-string 中 `{{` 是转义序列，`{{` → `{`
- **修复**: 将 `shortcode_open = "{{< inline_style >}}"` 改为普通字符串变量拼接

### 问题2: Hugo YAML frontmatter 解析失败
- **现象**: `value is not allowed in this context. map key-value is pre-defined` at line 2, col 32
- **根因**: 文章标题含中文引号 `"..."`（ASCII 双引号 U+0022），在 YAML 双引号字符串中未转义
- **修复**: `escape_yaml_str()` 函数对 ASCII `"` 转义为 `\"`

### 问题3: Hugo URL 小写
- **现象**: GitHub Pages 上的 URL 是 `/posts/npk8hbytuv0/`（小写）而非 `/posts/NPk8hbYTUv0/`
- **说明**: Hugo 默认将 URL 转为小写，这是正常行为，无需修复

## Git 提交记录

| Commit | 描述 |
|--------|------|
| `afc26fe` | 首次转换 20 个文章到 Hugo |
| `85c6016` | 生成 NPk8hbYTUv0 文章 |
| `9da7a48` | 转换全部 62 个 Hugo posts |
| `5eff849` | add Hugo auto-conversion to pipeline (v2.4) |
| `c2cf716` | fix: shortcode syntax in Hugo posts |
| `a97cb04` | fix: escape Chinese quotes in YAML frontmatter |
| `5599bc5` | pipeline v2.4 final |

## 验证结果

所有 13 个管道视频文章均已上线（2026-07-19 验证）:

| 视频 ID | 状态 | URL |
|---------|------|-----|
| NPk8hbYTUv0 | ✅ | https://yzwer.github.io/posts/npk8hbytuv0/ |
| 4dc6IvX9Y8g | ✅ | https://yzwer.github.io/posts/4dc6ivx9y8g/ |
| 4AU5d5l7CPw | ✅ | https://yzwer.github.io/posts/4au5d5l7cpw/ |
| iyjwRPNM0L4 | ✅ | https://yzwer.github.io/posts/iyjwrpnm0l4/ |
| PWUXT-Ohntk | ✅ | https://yzwer.github.io/posts/pwuxt-ohntk/ |
| LOXQXHHRUvU | ✅ | https://yzwer.github.io/posts/loxqxhhruvu/ |
| y5lMWdt5ak8 | ✅ | https://yzwer.github.io/posts/y5lmwdt5ak8/ |
| 9iD-GchCgaM | ✅ | https://yzwer.github.io/posts/9id-gchcgam/ |
| cpzVOkT3O_c | ✅ | https://yzwer.github.io/posts/cpzvokt3o_c/ |
| T3KyTslODKg | ✅ | https://yzwer.github.io/posts/t3kytslodkg/ |
| Tw45Kt-cGp4 | ✅ | https://yzwer.github.io/posts/tw45kt-cgp4/ |
| IPxckmi3Iqo | ✅ | https://yzwer.github.io/posts/ipxckmi3iqo/ |
| xQsiFRlzOjY | ✅ | https://yzwer.github.io/posts/xqsifrlzojy/ |

## 剩余待办

- [ ] 微信草稿上传（errcode 40164，IP 白名单问题，需在合规出口 IP 下执行）
- [ ] GitHub Pages 自定义域名（当前为空）
- [ ] Hugo workflow 可考虑升级到最新 Hugo 版本
