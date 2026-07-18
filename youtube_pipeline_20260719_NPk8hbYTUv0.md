# YouTube 管道运行记录 - 2026-07-19 01:15 (Cron 触发)

## 运行结果
- **触发**: Cron `每日YouTube视频检查+公众号文章生成`
- **时间**: 2026-07-19 01:15 (Asia/Shanghai)
- **管道版本**: run_pipeline.py v2.3

## 发现的新视频
- **视频ID**: `NPk8hbYTUv0`
- **标题**: 最危险的时刻，还没过去
- **内容**: 2026-07-17 A股单日暴跌深度分析（沪指跌3.05%破3800点，创业板跌7.15%，科创50跌7.12%）

## 处理结果
1. ✅ 下载视频 (102MB mp4, 本地保存，gitignore 排除)
2. ✅ 提取音频 (30MB wav, 本地保存，gitignore 排除)
3. ✅ Whisper 转录 (base 模型, 12550 字符)
4. ✅ 更新 last_video.txt
5. ✅ Git 集成推送（run_pipeline.py 新增 git push 逻辑首次实战成功）
   - Commit: `282c7c2` "youtube: pipeline run 2026-07-19 01:20" (283 files, 含历史未跟踪文件)
   - Push: 成功同步到 GitHub master
6. ✅ 生成公众号文章 HTML（10章节，红黑渐变模板）
   - 文件: `NPk8hbYTUv0_wechat_article.html` (10KB)
   - Commit: `85c6016` "youtube: NPk8hbYTUv0 wechat article"
   - Push: 成功同步到 GitHub（18797 字节）

## SSH Push 集成进展
- 完整搭建 SOCKS5 隧道方案：`ssh_via_socks5.py` + `~/.ssh/config` ProxyCommand
- 验证结果：TCP 隧道可建立，但 GitHub 在收到 SSH 版本字符串后立即关闭连接
- **根因**：Clash 代理出口 IP (27.44.20.159) 被 GitHub 限制 SSH 端口 22 访问
- **结论**：当前网络 SSH push 不可用，改用 HTTPS + token 推送（已验证工作）

## run_pipeline.py 改动
在 `main()` 末尾新增 git push 逻辑：
- 检测未提交变更 (`git status --porcelain`)
- 有变更则 `git add -A youtube_videos/` + `git commit` + `git push origin master`
- 使用 `GIT_HTTP_PROXY=http://127.0.0.1:6789` 环境变量走代理
- 失败仅记录警告，不中断管道

## 草稿上传状态
- ⏳ 所有 13 个视频（含 NPk8hbYTUv0）的公众号草稿上传仍被微信 API 阻断
- **原因**: errcode 40164（出口 IP 不在公众号 IP 白名单）
- **待办**: 需在合规 IP 环境下运行 `upload_draft.py <video_id>` 批量补传

## 完整视频清单（截至 2026-07-19）
已处理并推送至 GitHub 的视频（13个）：
y5lMWdt5ak8, 9iD-GchCgaM, cpzVOkT3O_c, T3KyTslODKg, 4dc6IvX9Y8g, Tw45Kt-cGp4, LOXQXHHRUvU, iyjwRPNM0L4, IPxckmi3Iqo, 4AU5d5l7CPw, PWUXT-Ohntk, xQsiFRlzOjY, NPk8hbYTUv0

所有文章均已生成并推送；草稿上传待合规 IP 环境。
