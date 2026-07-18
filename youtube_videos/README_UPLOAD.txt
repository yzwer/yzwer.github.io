SunRiches 公众号文章积压手动上传说明
========================================

【问题说明】
微信公众号API的IP白名单限制（errcode 40164）导致自动上传失败。
所有文章HTML已生成，现在需要手动复制粘贴到公众号后台。

【积压文章列表】(按生成时间排序，最新的在前)

01. _8vzIMnjny4   欧盟准备与中国"开战"           2026-06-05
02. LHSOm58ylBI   失联女大学生事件               2026-06-04
03. vH7rDhyn1W8   他这次打算干什么？             2026-06-03
04. pIgVOcpjFOY   最新数据揭示更严重问题         2026-06-03
05. fVaQ8vehaEo   Geng反伪运动人物被封号         2026-06-02
06. oDq9hCzzEng   伊朗局势分析                  2026-06-01
07. _260064XYuQ   新一轮地产救市                2026-05-31
08. eONVYvBxkyQ   救灾为什么这么难？             2026-05-30
09. JCyCN9x0JEc   国务院18天两派调查组          2026-05-28
10. 1OEIQTj_5QY   华为掏定律分析                2026-05-27
11. f-uXjRn19uU   上海交大"凡小姐"事件          2026-05-25
12. s_MKH36lhgg   湖北"白血病村"调查           2026-05-25
13. RYq2pdfv8l0   朝鲜修宪解读                  2026-05-25
14. ExxZ-ug-LFs   伯克希尔2025股东大会           2026-05-25
15. _gn03Q1qxtw   漳州杨梅泡药事件              2026-05-25
16. o-S-ibIBvrk   黄金剧烈波动                  2026-05-24
17. DqDUrNyLxZM   (视频较短)                    2026-05-24
18. CNbss-pyc18   (待确认)                      2026-05-17
19. cUwEpv2EGaQ   OPPO千亿手机厂商分析          2026-05-17
20. sojKNj_uXYU   (早期视频)                    2026-05-18之前

【手动上传步骤】

方法一：逐个复制（推荐）

1. 打开微信公众号后台：https://mp.weixin.qq.com
2. 点击左侧"内容与互动" → "图文消息"
3. 点击"新建图文消息"
4. 在正文区域粘贴HTML内容（文件中的<body>...</body>部分）
5. 设置标题（从文件名读取或查看文件内<title>标签）
6. 提取封面图：每个视频对应 {video_id}_cover.jpg
   （封面图在 youtube_videos/ 目录）
7. 点击"保存"或"群发"

方法二：直接导入HTML

1. 公众号后台 → 新建图文
2. 点击富文本编辑器右上角"源码"按钮（</>图标）
3. 复制HTML文件中的<body>...</body>内容粘贴进去
4. 切换回富文本模式查看效果

【快速定位】

每个视频对应的文章文件：
- 文件名格式：{video_id}_wechat_article.html
- 封面图：{video_id}_cover.jpg
- 两者在同一目录：C:\Users\11132\.qclaw\workspace-yw3plsutb1jupnif\youtube_videos\

【封面图列表】

已生成的封面图（jpg文件）：
_8vzIMnjny4_cover.jpg
LHSOm58ylBI_cover.jpg
vH7rDhyn1W8_cover.jpg
pIgVOcpjFOY_cover.jpg
fVaQ8vehaEo_cover.jpg
oDq9hCzzEng_cover.jpg
_260064XYuQ_cover.jpg
eONVYvBxkyQ_cover.jpg
JCyCN9x0JEc_cover.jpg
1OEIQTj_5QY_cover.jpg
f-uXjRn19uU_cover.jpg
s_MKH36lhgg_cover.jpg
RYq2pdfv8l0_cover.jpg
ExxZ-ug-LFs_cover.jpg
_gn03Q1qxtw_cover.jpg
o-S-ibIBvrk_cover.jpg
CNbss-pyc18_cover.jpg
cUwEpv2EGaQ_cover.jpg

【自动上传修复方案】

若希望恢复自动上传，需在微信公众平台添加当前出口IP到白名单：
IP: 112.93.223.39

添加路径：mp.weixin.qq.com → 设置与开发 → 基本配置 → IP白名单 → 修改

添加后告诉我，我可以立即批量上传所有积压文章！

========================================
生成时间: 2026-06-05
