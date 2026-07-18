import re

HTML_FILE = r"C:\Users\11132\.qclaw\workspace-yw3plsutb1jupnif\youtube_videos\sojKNj_uXYU_wechat_article.html"

# 读取文件
with open(HTML_FILE, 'r', encoding='utf-8') as f:
    content = f.read()

# 提取当前标题（用于确认）
title_match = re.search(r'<title>([^<]+)</title>', content)
current_title = title_match.group(1) if title_match else 'NOT FOUND'
print(f"当前标题: {current_title}\n")

# 根据内容生成自创标题
# 这篇文章讲的是：南极游轮汉坦病毒事件，死亡率30-60%，人传人争议
new_title = "南极游轮病毒事件调查：汉坦病毒的真相与误读"

print(f"新标题: {new_title}\n")

# 更新 <title> 标签
content = re.sub(r'<title>[^<]+</title>', f'<title>{new_title}</title>', content)

# 更新封面大标题（ct-title 类）
content = re.sub(
    r'<div class="ct-title">[^<]+</div>',
    f'<div class="ct-title">{new_title}</div>',
    content
)

# 保存
with open(HTML_FILE, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"✅ 标题已更新！")
print(f"文件: {HTML_FILE}")
